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
from proksee.species import Species


def estimate_species_from_estimations(estimations, min_shared_fraction, min_identity, min_multiplicity,
                                      ignore_viruses=True):
    """
    Estimates which species are present in a list of Estimations. Species will be reported if their associated
    estimation's measurements pass the thresholds passed to this function. The species will be sorted in descending
    order of confidence.

    PARAMETERS
        estimations (List(Estimation)): a list of species estimations from which to determine which species
            present in the data (according to the provided threshold values)
        min_shared_fraction (float): the minimum fraction of shared hashes
        min_identity (float): the minimum identity; estimation of fraction of bases shared between reads and genome
        min_multiplicity (int): the median multiplicity; relates to coverage and redundancy of observations
        ignore_viruses (bool=True): whether or not to ignore virus estimations

    RETURNS
        species (List(Species)): a list of major species determined from the estimations
    """

    species = []

    for estimation in estimations:

        full_taxonomy = str(estimation.full_taxonomy)

        if ignore_viruses and full_taxonomy.startswith("Viruses"):
            continue

        shared_hashes = estimation.shared_hashes
        identity = estimation.identity
        median_multiplicity = estimation.median_multiplicity

        if shared_hashes >= min_shared_fraction and identity >= min_identity and median_multiplicity \
                >= min_multiplicity:

            species.append(estimation.species)

    return species


class SpeciesEstimator:
    """
    This class represents a species estimation tool.

    ATTRIBUTES
        input_list (List(str)): a list of input files; this will likely be one or two FASTQ file locations
        output_directory (str): the directory to use for output
    """

    def __init__(self, input_list, output_directory):
        """
        Initializes the species estimator.

        PARAMETERS
            input_list (List(str)): a list of input files; this will likely be one or two FASTQ file locations
            output_directory (str): the directory to use for program output
        """

        self.input_list = [i for i in input_list if i]  # remove all "None" inputs
        self.output_directory = output_directory

    def estimate_major_species(self):
        """
        Estimates the major species present in the reads. If this function returns more than one "major" species, then
        it is possible there is major contamination in the input data.

        RETURNS
            species (List(Species)): a list of the estimated major species, sorted in descending order of most complete
                and highest covered; will contain an "Unknown" species if no major species was found
        """

        MIN_SHARED_FRACTION = 0.90
        MIN_IDENTITY = 0.90
        MIN_MULTIPLICITY = 5

        refseq_masher_filename = self.run_refseq_masher()
        estimations = parse_species_from_refseq_masher(refseq_masher_filename)

        species = estimate_species_from_estimations(estimations, MIN_SHARED_FRACTION, MIN_IDENTITY, MIN_MULTIPLICITY)

        if len(species) == 0:
            species.append(Species("Unknown", 0.0))

        return species

    def estimate_all_species(self):
        """
        Estimates all the species present in the reads.

        RETURNS
            species (List(Species)): a list of all estimated species, sorted in descending order of most complete
                and highest covered; will contain an "Unknown" species if no species were found
        """

        MIN_SHARED_FRACTION = 0
        MIN_IDENTITY = 0
        MIN_MULTIPLICITY = 0

        refseq_masher_filename = self.run_refseq_masher()
        estimations = parse_species_from_refseq_masher(refseq_masher_filename)

        species = estimate_species_from_estimations(estimations, MIN_SHARED_FRACTION, MIN_IDENTITY, MIN_MULTIPLICITY)

        if len(species) == 0:
            species.append(Species("Unknown", 0.0))

        return species

    def run_refseq_masher(self):
        """
        Runs RefSeq Masher on the input data.

        POST
            If successful, RefSeq Masher will have executed on the input and the output will be written to the output
            directory. If unsuccessful, the output file we be empty. It is necessary to check to see if the output file
            contains any output.
        """

        output_filename = os.path.join(self.output_directory, "refseq_masher.o")
        error_filename = os.path.join(self.output_directory, "refseq_masher.e")

        output_file = open(output_filename, "w")
        error_file = open(error_filename, "w")

        # create the refseq_masher command
        command = "refseq_masher contains -i 0 -v 1"

        for item in self.input_list:
            command += " " + str(item)

        # run refseq_masher
        try:
            subprocess.check_call(command, shell=True, stdout=output_file, stderr=error_file)

        except subprocess.CalledProcessError:
            pass  # it will be the responsibility of the calling function to insure there was output

        finally:
            output_file.close()
            error_file.close()

        return output_filename
