"""
Copyright Government of Canada 2022

Written by:

Eric Marinier
    National Microbiology Laboratory, Public Health Agency of Canada

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

from proksee import utilities
from proksee.assembly_database import AssemblyDatabase
from proksee.assembly_measurer import AssemblyMeasurer
from proksee.heuristic_evaluator import HeuristicEvaluator
from proksee.machine_learning_evaluator import MachineLearningEvaluator


def evaluate(contigs_filename, output_directory, database_path, mash_database_path,
             id_mapping_filename, species_name=None):
    """
    Evaluates the quality of a provided sequence assembly.

    ARGUMENTS:
        contigs_filename (string): the filename of the contigs to evaluate
        output_directory (string): the location to place all program output and temporary files
        database_path (string): the file path of the sequence assembly statistics database
        mash_database_path (string): optional; the name of the Mash database
        id_mapping_filename (string) optional; the name of the NCBI ID-to-taxonomy mapping (table) file
        species_name (string): optional; the name of the species being assembled

    POST:
        The contigs with passed filename will be evaluated and the results will be written to standard output.
    """

    # Make output directory:
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    # Species and assembly database:
    assembly_database = AssemblyDatabase(database_path)

    # Estimate species
    species_list = utilities.determine_species([contigs_filename], assembly_database, output_directory,
                                               mash_database_path, id_mapping_filename, species_name)
    species = species_list[0]
    print("The identified species is: " + str(species.name) + "\n")

    # Measure assembly quality statistics:
    assembly_measurer = AssemblyMeasurer(contigs_filename, output_directory)
    assembly_quality = assembly_measurer.measure_quality()

    # Heuristic evaluation:
    evaluator = HeuristicEvaluator(species, assembly_database)
    evaluation = evaluator.evaluate(assembly_quality)
    print(evaluation.report)

    # Machine learning evaluation:
    evaluator = MachineLearningEvaluator(species)
    evaluation = evaluator.evaluate(assembly_quality)
    print(evaluation.report)

    print("\nComplete.\n")
