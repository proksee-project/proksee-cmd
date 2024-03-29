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
from proksee.utilities import InputType
from proksee.utilities import get_time

from proksee.assembly_database import AssemblyDatabase
from proksee.assembly_measurer import AssemblyMeasurer
from proksee.machine_learning_evaluator import MachineLearningEvaluator

import proksee.config as config
from proksee.ncbi_assembly_evaluator import NCBIAssemblyEvaluator
from proksee.species_assembly_evaluator import SpeciesAssemblyEvaluator
from proksee.resource_specification import ResourceSpecification

DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                             "refseq_short.csv")
ID_MAPPING_FILENAME = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                                   "mash_id_mapping.tab.gz")


@click.command('evaluate',
               short_help='Evaluates the quality of an assembly.')
@click.argument('contigs', required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-s', '--species', required=False, default=None,
              help="The species to assemble. This will override species estimation. Must be spelled correctly.")
@click.option('--min-contig-length', required=False, default=1000,
              help="The minimum contig length to include in analysis and output. The default is 1000.")
@click.option('-o', '--output', required=True,
              type=click.Path(exists=False, file_okay=False,
                              dir_okay=True, writable=True))
@click.option('-t', '--threads', required=False, default=4, type=click.IntRange(min=1, max=None),
              help="Specifies the number of threads programs in the pipeline should use. The default is 4.")
@click.option('-m', '--memory', required=False, default=4, type=click.IntRange(min=1, max=None),
              help="Specifies the amount of memory in gigabytes programs in the pipeline should use. The default is 4")
@click.pass_context
def cli(ctx, contigs, species, min_contig_length, output, threads, memory):

    # Check Mash database is installed:
    mash_database_path = config.get(config.MASH_PATH)

    if not os.path.isfile(mash_database_path):
        print("Please run 'proksee updatedb' to install the databases!")
        return

    resource_specification = ResourceSpecification(threads, memory)
    evaluate(contigs, output, resource_specification, mash_database_path, species, min_contig_length)


def evaluate(contigs_filename, output_directory, resource_specification, mash_database_path,
             species_name=None, minimum_contig_length=1000, id_mapping_filename=ID_MAPPING_FILENAME):
    """
    The main control flow of the program that evaluates the assembly.

    ARGUMENTS:
        contigs_filename (string): the filename of the contigs to evaluate
        output_directory (string): the location to place all program output and temporary files
        resource_specification (ResourceSpecification): the computational resources available
        mash_database_path (string): optional; the name of the Mash database
        species_name (string): optional; the name of the species being assembled
        minimum_contig_length (int): optional; the minimum contig length to consider for analysis
        id_mapping_filename (string) optional; the name of the NCBI ID-to-taxonomy mapping (table) file

    POST:
        The contigs with passed filename will be evaluated and the results will be written to standard output.
    """

    click.echo("\n" + get_time())
    click.echo(utilities.build_version_message())

    # Make output directory:
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    # Species and assembly database:
    assembly_database = AssemblyDatabase(DATABASE_PATH)

    # Estimate species
    species_list = utilities.determine_major_species([contigs_filename], assembly_database, output_directory,
                                                     mash_database_path, id_mapping_filename, InputType.ASSEMBLY,
                                                     resource_specification, species_name)
    species = species_list[0]

    click.echo("\n" + get_time())
    click.echo("The identified species is: " + str(species.name) + "\n")

    # Measure assembly quality statistics:
    assembly_measurer = AssemblyMeasurer(contigs_filename, output_directory, minimum_contig_length)
    assembly_quality = assembly_measurer.measure_quality()

    # Heuristic evaluation:
    species_evaluator = SpeciesAssemblyEvaluator(species, assembly_database)
    species_evaluation = species_evaluator.evaluate_assembly_from_database(assembly_quality)

    click.echo("\n" + get_time())
    click.echo(species_evaluation.report)

    ncbi_evaluator = NCBIAssemblyEvaluator(species, assembly_database)
    ncbi_evaluation = ncbi_evaluator.evaluate_assembly_from_fallback(assembly_quality)

    click.echo("\n" + get_time())
    click.echo(ncbi_evaluation.report)

    # Machine learning evaluation:
    evaluator = MachineLearningEvaluator(species)
    evaluation = evaluator.evaluate(assembly_quality)
    click.echo(evaluation.report)

    click.echo("\n" + get_time())
    click.echo("Complete.\n")
