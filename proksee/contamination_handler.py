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
    """

    def __init__(self, species, contigs_file, output_directory):
        """
        Initializes the contamination handler.

        PARAMETERS
            species (Species): the species that is believed to be the major (i.e. correct, non-contaminate) species
            contigs_file (str): the file location of assembled contigs to check for contamination
            output_directory (str): the output directory for the program
        """

        self.species = species
        self.contigs_file = contigs_file
        self.output_directory = output_directory

    def estimate_contamination(self):
        """
        Estimates species contamination in the contigs by examining the five largest contigs and looking for
        disagreement between the species provided and the species estimated for each contig.

        RETURNS
            evaluation (Evaluation): an Evaluation of whether or not the data passes / succeeds a contamination "test";
                contains an associated, plain-language report
        """

        FASTA_DIRECTORY = "fasta"
        MAX_CONTIGS_EVALUATED = 5

        fasta_directory = os.path.join(self.output_directory, FASTA_DIRECTORY)

        # Split the multi-FASTA file into single-record FASTA files (contigs) and gather a list of file locations in
        # descending order by contig size:
        fasta_files = split_multi_fasta_into_fasta(self.contigs_file, fasta_directory)

        contig_species = []

        # Iterate through the list of contig file locations in descending order:
        for i in range(min(len(fasta_files), MAX_CONTIGS_EVALUATED)):

            species_estimator = SpeciesEstimator([fasta_files[i]], self.output_directory)
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

        if len(sorted_species) == 1 and species_list[0].name == Species.UNKNOWN:
            success = True
            report += "WARNING: Unable to confidently estimate the species from the assembled contigs.\n"

        elif len(sorted_species) == 1 and species_list[0] == self.species:
            success = True
            report += "PASS: The evaluated contigs appear to agree with the species estimation.\n"
            report += "      The estimated species is: " + str(self.species) + "\n"

        else:
            success = False
            report += "FAIL: The evaluated contigs don't appear to agree with the species estimation.\n"
            report += "      The estimated species is: " + str(self.species) + "\n"
            report += "      The following species were estimated from the contigs:\n\n"

            for species in sorted_species:
                report += "      " + str(species) + "\n"

        return Evaluation(success, report)
