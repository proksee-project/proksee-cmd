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

from proksee.parser.fasta_parser import split_multi_fasta_into_fasta
from proksee.species_estimator import SpeciesEstimator


class ContaminationFilterer:

    def __init__(self, contigs_file, output_directory):

        self.contigs_file = contigs_file
        self.output_directory = output_directory

    def filter_contigs(self):

        print("Hello!")

        fasta_directory = os.path.join(self.output_directory, "fasta")
        fasta_files = split_multi_fasta_into_fasta(self.contigs_file, fasta_directory)

        for fasta_file in fasta_files:
            print(fasta_file)

            species_estimator = SpeciesEstimator([fasta_file], self.output_directory)
            species_list = species_estimator.estimate_species()

            print(species_list[0])

        print("Done!")
