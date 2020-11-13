"""
Copyright Government of Canada 2020

Written by: Eric Marinier, National Microbiology Laboratory,
            Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import os
import subprocess

from proksee.parser.refseq_masher_parser import parse_species_from_refseq_masher


def estimate_major_species(classifications, ignore_viruses=True):
    """
    Estimates which major species are present. The species will be sorted in descending order of confidence. If there
    are multiple major species reported, then it is possible there is significant contamination.

    PARAMETERS
        classifications (List(Classification)): a list of species classifications from which to determine major species
            present in the data
        ignore_viruses (bool=True): whether or not to ignore virus classifications

    RETURNS
        species (List(Species)): a list of major species determined from the classifications
    """

    MIN_SHARED_FRACTION = 0.90  # the minimum fraction of shared hashes
    MIN_IDENTITY = 0.90  # the minimum identity; estimation of fraction of bases shared between reads and genome
    MIN_MULTIPLICITY = 5  # the median multiplicity; relates to coverage and redundancy of observations

    species = []

    for classification in classifications:

        full_taxonomy = str(classification.full_taxonomy)

        if ignore_viruses and full_taxonomy.startswith("Viruses"):
            continue

        shared_hashes = classification.shared_hashes
        identity = classification.identity
        median_multiplicity = classification.median_multiplicity

        if shared_hashes >= MIN_SHARED_FRACTION and identity >= MIN_IDENTITY and median_multiplicity \
                >= MIN_MULTIPLICITY:

            species.append(classification.species)

    return species


class SpeciesEstimator:
    """
    This class represents a species estimation tool.

    ATTRIBUTES
        forward (str): the filename of the forward reads
        reverse (str): the filename of the reverse reads
        output_directory (str): the directory to use for program output
    """

    def __init__(self, forward, reverse, output_directory):
        """
        Initializes the read classifier.

        PARAMETERS
            forward (str): the filename of the forward reads
            reverse (str): the filename of the reverse reads
            output_directory (str): the directory to use for program output
        """

        self.forward = forward
        self.reverse = reverse
        self.output_directory = output_directory

    def estimate_species(self):
        """
        Estimates the species present in the reads.

        RETURNS
            species (List(Species)): a list of the estimated major species
        """

        refseq_masher_filename = self.run_refseq_masher()
        classifications = parse_species_from_refseq_masher(refseq_masher_filename)

        species = estimate_major_species(classifications)

        for s in species:
            print(s)

        return species

    def run_refseq_masher(self):
        """
        Runs RefSeq Masher on the reads.

        POST
            If successful, RefSeq Masher will have executed on the reads and the output will be written to the output
            directory. If unsuccessful, an error message will be raised.
        """

        output_filename = os.path.join(self.output_directory, "refseq_masher.o")
        error_filename = os.path.join(self.output_directory, "refseq_masher.e")

        output_file = open(output_filename, "w")
        error_file = open(error_filename, "w")

        # create the refseq_masher command
        if self.reverse:
            command = "refseq_masher contains " + str(self.forward) + " " + str(self.reverse)
        else:
            command = "refseq_masher contains " + str(self.forward)

        # run refseq_masher
        try:
            subprocess.check_call(command, shell=True, stdout=output_file, stderr=error_file)

        except subprocess.CalledProcessError as e:
            raise e

        finally:
            output_file.close()
            error_file.close()

        return output_filename
