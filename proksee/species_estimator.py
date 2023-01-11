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

from proksee.parser.mash_parser import MashParser
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
        min_identity (float): the minimum identity; estimation of fraction of bases shared between the input data and
            genome
        min_multiplicity (int): the median multiplicity; relates to coverage and redundancy of observations
        ignore_viruses (bool=True): whether or not to ignore virus estimations

    RETURNS
        species (List(Species)): a list of major species determined from the estimations
    """

    species = []

    for estimation in estimations:

        superkingdom = estimation.species.superkingdom
        full_lineage = estimation.species.full_lineage

        if ignore_viruses and superkingdom.startswith("Virus"):
            continue

        if "unspecified" in full_lineage.lower():
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
        mash_database_filename (str): the filename of the Mash database
        id_mapping_filename (str): filename of the NCBI ID-to-taxonomy mapping file
    """

    OUTPUT_FILENAME = "mash.o"

    def __init__(self, input_list, output_directory, mash_database_filename, id_mapping_filename):
        """
        Initializes the species estimator.

        PARAMETERS
            input_list (List(str)): a list of input files; this will likely be one or two FASTQ file locations
            output_directory (str): the directory to use for program output
            mash_database_filename (str): the filename of the Mash database
            id_mapping_filename (str): filename of the NCBI ID-to-taxonomy mapping file
        """

        self.input_list = [i for i in input_list if i]  # remove all "None" inputs
        self.output_directory = output_directory
        self.mash_database_filename = mash_database_filename
        self.id_mapping_filename = id_mapping_filename

    def estimate_major_species(self):
        """
        Estimates the major species present in the input data. The input data will need to be in a form similar to
        sequencing reads (i.e. have multiplicity, or depth of coverage). If this function returns more than one "major"
        species, then it is possible there is major contamination in the input data.

        RETURNS
            species (List(Species)): a list of the estimated major species, sorted in descending order of most complete
                and highest covered; will contain an "Unknown" species if no major species was found
        """

        MIN_SHARED_FRACTION = 0.80
        MIN_IDENTITY = 0.90
        MIN_MULTIPLICITY = 5

        mash_filename = self.run_mash()
        mash_parser = MashParser(self.id_mapping_filename)
        estimations = mash_parser.parse_estimations(mash_filename)

        species = estimate_species_from_estimations(estimations, MIN_SHARED_FRACTION, MIN_IDENTITY, MIN_MULTIPLICITY)

        if len(species) == 0:
            species.append(Species(Species.UNKNOWN, 0.0))

        return species

    def estimate_all_species(self):
        """
        Estimates all the species present in the input data, with only minimal filtering for noise.

        RETURNS
            species (List(Species)): a list of all estimated species, sorted in descending order of most complete
                and highest covered; will contain an "Unknown" species if no species were found
        """

        MIN_SHARED_FRACTION = 0.015
        MIN_IDENTITY = 0
        MIN_MULTIPLICITY = 1

        mash_filename = self.run_mash()
        mash_parser = MashParser(self.id_mapping_filename)
        estimations = mash_parser.parse_estimations(mash_filename)

        species = estimate_species_from_estimations(estimations, MIN_SHARED_FRACTION, MIN_IDENTITY, MIN_MULTIPLICITY)

        if len(species) == 0:
            species.append(Species(Species.UNKNOWN, 0.0))

        return species

    def run_mash(self):
        """
        Runs Mash on the input data.

        RETURN
            mash_filename: the name of the Mash output file

        POST
            If successful, Mash will have executed on the input and an output file named "mash.output" to be parsed
            will be written to file.
        """

        LINE_LENGTH_LIMIT = 3500  # Actually 4095, but smaller here for safety.

        unsorted_output_filepath = os.path.abspath(os.path.join(self.output_directory,
                                                                self.OUTPUT_FILENAME + ".unsorted"))
        sorted_output_filepath = os.path.abspath(os.path.join(self.output_directory,
                                                              self.OUTPUT_FILENAME))

        # Find the common directory between all paths:
        # This is a safer solution than assuming everything will always use the output directory.
        common_path = os.path.commonpath(self.input_list)

        if os.path.isdir(common_path):
            common_directory = common_path
        else:
            # The common path is NOT a directory.
            # This can happen when there is only a single input (the common path is the single file's filepath).
            common_directory = os.path.dirname(common_path)

        # create the mash command
        # Use the full file path for the database file:
        command = ["mash", "screen", "-i", "0", "-v", "1", self.mash_database_filename]

        for item in self.input_list:
            # Grab the relative path from the common directory of each item:
            command.append(str(os.path.relpath(item, start=common_directory)))

            # Break loop if command line argument is getting too long.
            # This behaviour is likely fine for now, since the contigs are organized by size
            # and the missed contigs will likely be uninformative.
            if len(command) >= LINE_LENGTH_LIMIT:
                break

        # run mash
        try:
            with open(unsorted_output_filepath, 'w') as unsorted_output_file, \
                 open(sorted_output_filepath, 'w') as sorted_output_file, \
                 open(os.devnull, 'w') as NULL:

                # Run relative to the output directory so that filepaths are shorter:
                subprocess.run(command, shell=False, encoding="utf8", cwd=common_directory,
                               stdout=unsorted_output_file, stderr=NULL)

                # Sort the output:
                subprocess.run(["sort", "-gr", str(unsorted_output_file)], shell=False, encoding="utf8",
                               stdout=sorted_output_file, stderr=NULL)

                # Remove the unsorted file:
                os.remove(unsorted_output_filepath)

        except subprocess.CalledProcessError:
            pass  # it will be the responsibility of the calling function to ensure there was output

        return sorted_output_filepath
