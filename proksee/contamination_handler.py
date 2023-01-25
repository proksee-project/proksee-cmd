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

from proksee.evaluation import Evaluation
from proksee.parser.fasta_parser import split_multi_fasta_into_fasta
from proksee.species_estimator import SpeciesEstimator
from proksee.species import Species


class ContaminationHandler:
    """
    This class represents a contamination handler, a tool responsible for identifying, filtering, and otherwise
    handling contamination in the data.

    ATTRIBUTES
        species (str): the species that is believed to be the major (i.e. correct, non-contaminate) species
        contigs_file (str): the file location of assembled contigs to check for contamination
        output_directory (str): the directory location to write single-record FASTA files; this will probably be a
            subdirectory of the program output directory
        mash_database_filename (str): the filename of the Mash sketch (database)
        id_mapping_filename (str): filename of the NCBI ID-to-taxonomy mapping file
        resource_specification (ResourceSpecification): the computational resources available
    """

    FASTA_DIRECTORY = "fasta"

    def __init__(self, species, contigs_file, output_directory, mash_database_filename, id_mapping_filename,
                 resource_specification):
        """
        Initializes the contamination handler.

        PARAMETERS
            species (Species): the species that is believed to be the major (i.e. correct, non-contaminate) species
            contigs_file (str): the file location of assembled contigs to check for contamination
            output_directory (str): the output directory for the program
            mash_database_filename (str): the filename of the Mash sketch (database)
            id_mapping_filename (str): filename of the NCBI ID-to-taxonomy mapping file
            resource_specification (ResourceSpecification): the computational resources available
        """

        self.species = species
        self.contigs_file = contigs_file
        self.output_directory = output_directory
        self.mash_database_filename = mash_database_filename
        self.id_mapping_filename = id_mapping_filename
        self.resource_specification = resource_specification

    def estimate_contamination(self):
        """
        Estimates species contamination in the contigs organizing the contigs into five groups and looking for
        disagreement between the species provided and the species estimated for each contig group.

        RETURNS
            evaluation (Evaluation): an Evaluation of whether or not the data passes / succeeds a contamination "test";
                contains an associated, plain-language report
        """

        # The single FASTA file containing multiple contigs (self.contigs_file) is first
        # split into multiple single contig FASTA files, which are all placed in the
        # newly created `fasta_directory`.
        #
        # Next, a number of chunks / lists are created. The single contig FASTA files
        # are listed in descending order by contig size and this allows for (usually)
        # an even distribution of contigs by size into the different chunks / lists.
        # Single contig FASTA files are added to each chunk by rotating the lists and
        # added the next largest contig. At the end of this step, there should be a
        # number of lists equal to the number of chunks, and each list should contain
        # a similar amount of sequence.
        #
        # Finally, the species of each chunk / list is evaluated independently. This
        # will consider all of the single contig FASTA files in the chunk together
        # when estimating a species. For example, if there are 5 chunks, each will
        # contain approxately 1/5th of the total assembly sequence, and each 1/5th
        # will be given a species estimation. These 5 species estimations will then be
        # compared with each other and the provided species to see if there's any
        # discrepancey. What this accomplishes is distributing the entire collection
        # of assembled contigs into 5 different chunks, estimating the species of
        # each chunk, and ensuring that each chunk still provides the same species
        # estimation.
        #
        # The motivation is that with that right number of chunks (accounting for
        # computational time), we should observe if a large contiminate contig has
        # been assembled, because it will disagree with the other chunks and the
        # provided species.

        CHUNKS = 5

        fasta_directory = os.path.join(self.output_directory, self.FASTA_DIRECTORY)

        # Split the multi-FASTA file into single-record FASTA files (contigs) and gather a list of file locations in
        # descending order by contig size:
        fasta_files = split_multi_fasta_into_fasta(self.contigs_file, fasta_directory)
        num_contigs = len(fasta_files)

        contig_species = []
        contig_filenames = []  # A list of (filename) lists

        # Create the list of lists:
        # Take minimum of CHUNKS and number of contigs, otherwise we get empty chunks.
        for i in range(min(CHUNKS, num_contigs)):
            contig_filenames.append([])

        # Evenly distribute the FASTA filenames to the lists:
        # (Reminder the FASTA filenames are sorted in descending order by contig length.)
        for i in range(len(fasta_files)):

            index = i % CHUNKS  # Modulus division to "rotate" the index.
            contig_filenames[index].append(fasta_files[i])

        # Iterate through the list of contig file locations in descending order:
        for i in range(len(contig_filenames)):

            species_estimator = SpeciesEstimator(contig_filenames[i], self.output_directory,
                                                 self.mash_database_filename, self.id_mapping_filename,
                                                 self.resource_specification)
            species_list = species_estimator.estimate_all_species()

            contig_species.append(species_list[0])  # Select the estimation with the most evidence

        evaluation = self.evaluate_species(contig_species)

        return evaluation

    def evaluate_species(self, species_list):
        """
        Evaluates the species for contamination. That is, checks for disagreement with the major species
        and any observed species in the passed list.

        PARAMETERS
            species_list (List (Species)): a list of species to compare against the major species

        RETURNS
            evaluation (Evaluation): an Evaluation of whether or not the data passes / succeeds a contamination "test";
                contains an associated, plain-language report
        """

        sorted_species = list(set(species_list))  # Convert to set and back to list to find only unique species
        sorted_species.sort(key=lambda item: item.confidence, reverse=True)  # "item" is an Species

        report = "\n"

        # Species couldn't be estimated from reads:
        if self.species.name == Species.UNKNOWN:
            success = True
            report += "WARNING: Unable to determine contamination as a species could not be estimated from the reads.\n"

            # Some species were estimation from the contigs:
            if len(sorted_species) > 0:
                report += "         The following species were estimated from the contigs:\n\n"

                for species in sorted_species:
                    report += "         " + str(species) + "\n"

        # Species was estimated from reads, but couldn't be estimated from contigs:
        elif len(sorted_species) == 1 and species_list[0].name == Species.UNKNOWN:
            success = True
            report += "WARNING: Unable to confidently estimate the species from the assembled contigs.\n"

        # Species was estimated from reads, and estimation from contigs matches:
        elif len(sorted_species) == 1 and species_list[0] == self.species:
            success = True
            report += "PASS: The evaluated contigs appear to agree with the species estimation.\n"
            report += "      The estimated species is: " + str(self.species) + "\n"

        # Species was estimated from reads, but at least one estimation does not match:
        else:
            success = False
            report += "FAIL: The evaluated contigs don't appear to agree with the species estimation.\n"
            report += "      The estimated species is: " + str(self.species) + "\n"
            report += "      The following species were estimated from the contigs:\n\n"

            for species in sorted_species:
                report += "      " + str(species) + "\n"

        return Evaluation(success, report)
