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

from proksee.assembly_database import AssemblyDatabase
from proksee.assembly_measurer import AssemblyMeasurer
from proksee.heuristic_evaluator import HeuristicEvaluator
from proksee.machine_learning_evaluator import MachineLearningEvaluator
from proksee.species import Species
from proksee.species_estimator import SpeciesEstimator

DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                             "database.csv")


def determine_species(contigs_filename, assembly_database, output_directory, species_name=None):
    """
    Attempts to determine the species in the contigs.

    ARGUMENTS:
        contigs_filename (string): the contigs to determine the species from
        assembly_database (AssemblyDatabase): the assembly database
        output_directory (string): the location  of the output directory -- for placing temporary output
        species_name (string): optional; the scientific name of the species

    RETURNS:
        species_list (List(Species)): a list of major species estimated to be present in the contigs
    """

    species_list = None

    if species_name:
        if assembly_database.contains(species_name):
            click.echo("\nThe species '" + str(species_name) + "' was recognized.")
            species_list = [Species(species_name, 1.0)]

        else:
            click.echo("\nThe species name '" + str(species_name) + "' is unrecognized.")

    if species_list is None:
        click.echo("\nAttempting to identify the species from the contigs.")

        input_file_locations = [contigs_filename]  # Needs to be a list.
        species_estimator = SpeciesEstimator(input_file_locations, output_directory)
        species_list = species_estimator.estimate_all_species()

    return species_list


@click.command('evaluate',
               short_help='Evaluates the quality of an assembly.')
@click.argument('contigs', required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-o', '--output', required=True,
              type=click.Path(exists=False, file_okay=False,
                              dir_okay=True, writable=True))
@click.pass_context
def cli(ctx, contigs, output):
    evaluate(contigs, output)


def evaluate(contigs_filename, output_directory):
    """
    The main control flow of the program that evaluates the assembly.

    ARGUMENTS:
        contigs_filename (string): the filename of the contigs to evaluate
        output_directory (string): the location to place all program output and temporary files

    POST:
        The contigs with passed filename will be evaluated and the results will be written to standard output.
    """

    # Species and assembly database:
    assembly_database = AssemblyDatabase(DATABASE_PATH)

    # Estimate species
    species_list = determine_species(contigs_filename, assembly_database, output_directory, None)
    species = species_list[0]
    click.echo("The identified species is: " + str(species.name) + "\n")

    # Measure assembly quality statistics:
    assembly_measurer = AssemblyMeasurer(contigs_filename, output_directory)
    assembly_quality = assembly_measurer.measure_quality()

    # Heuristic evaluation:
    evaluator = HeuristicEvaluator(species, assembly_quality, assembly_database)
    evaluation = evaluator.evaluate()
    print(evaluation.report)

    # Machine learning evaluation:
    evaluator = MachineLearningEvaluator(species, assembly_quality)
    evaluation = evaluator.evaluate()
    click.echo(evaluation.report)

    click.echo("\nComplete.\n")
