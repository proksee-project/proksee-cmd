"""
Copyright Government of Canada 2021

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

import click
import os

from pathlib import Path

from proksee import utilities
from proksee.assembly_database import AssemblyDatabase
from proksee.assembly_measurer import AssemblyMeasurer
from proksee.heuristic_evaluator import HeuristicEvaluator
from proksee.machine_learning_evaluator import MachineLearningEvaluator

DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                             "refseq_short.csv")
MASH_DATABASE = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                             "refseq.genomes.k21s1000.msh")
ID_MAPPING_FILENAME = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                                   "mash_id_mapping.tab.gz")


@click.command('evaluate',
               short_help='Evaluates the quality of an assembly.')
@click.argument('contigs', required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-s', '--species', required=False, default=None,
              help="The species to assemble. This will override species estimation. Must be spelled correctly.")
@click.option('-o', '--output', required=True,
              type=click.Path(exists=False, file_okay=False,
                              dir_okay=True, writable=True))
@click.pass_context
def cli(ctx, contigs, output, species):

    # Check Mash database is installed:
    if not os.path.isfile(MASH_DATABASE):
        print("Please run 'proksee updatedb' to install the databases!")
        return

    evaluate(contigs, output, species)


def evaluate(contigs_filename, output_directory, species_name=None,
             mash_database_filename=MASH_DATABASE,
             id_mapping_filename=ID_MAPPING_FILENAME):
    """
    The main control flow of the program that evaluates the assembly.

    ARGUMENTS:
        contigs_filename (string): the filename of the contigs to evaluate
        output_directory (string): the location to place all program output and temporary files
        species_name (string): optional; the name of the species being assembled
        mash_database_filename (string): optional; the name of the Mash database
        id_mapping_filename (string) optional; the name of the NCBI ID-to-taxonomy mapping (table) file

    POST:
        The contigs with passed filename will be evaluated and the results will be written to standard output.
    """

    click.echo(utilities.build_version_message())

    # Make output directory:
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    # Species and assembly database:
    assembly_database = AssemblyDatabase(DATABASE_PATH)

    # Estimate species
    species_list = utilities.determine_species([contigs_filename], assembly_database, output_directory,
                                               mash_database_filename, id_mapping_filename, species_name)
    species = species_list[0]
    click.echo("The identified species is: " + str(species.name) + "\n")

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
    click.echo(evaluation.report)

    click.echo("\nComplete.\n")
