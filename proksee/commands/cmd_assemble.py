"""
Copyright Government of Canada 2020

Written by:

Arnab Saha Mandal
    University of Manitoba
    National Microbiology Laboratory, Public Health Agency of Canada

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

from proksee.assembly_evaluator import AssemblyEvaluator, evaluate_assembly, compare_assemblies
from proksee.assembly_database import AssemblyDatabase
from proksee.contamination_handler import ContaminationHandler
from proksee.input_verification import are_valid_fastq
from proksee.reads import Reads
from proksee.species_estimator import SpeciesEstimator
from proksee.platform_identify import PlatformIdentifier
from proksee.read_filterer import ReadFilterer
from proksee.expert_system import ExpertSystem
from proksee.writer.assembly_statistics_writer import AssemblyStatisticsWriter

DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                             "database.csv")


def report_valid_fastq(valid):
    """
    Reports to output whether or not the reads appear to be in a valid FASTQ file format.

    ARGUMENTS
        valid (bool): whether or not the reads appear to be in FASTQ format

    POST
        A statement reporting whether or not the reads appear to be in a valid FASTQ file format will be written to the
        program's output.
    """

    if not valid:
        output = "One or both of the reads are not in FASTQ format."

    else:
        output = "The reads appear to be formatted correctly."

    click.echo(output)


def report_platform(platform):
    """
    Reports the sequencing platform to output.

    ARGUMENTS
        platform (Platform (Enum)): the sequencing platform to report

    POST
        A statement reporting the sequencing platform will be written to output.
    """

    output = "SEQUENCING PLATFORM: " + str(platform.value) + "\n"

    click.echo(output)


def report_species(species_list):
    """
    Reports observed species in the reads to output.

    ARGUMENTS
        species_list (List(Species)): the list of species to report

    POST
        The observed species will be reported to output.
    """

    species = species_list[0]
    click.echo("SPECIES: " + str(species))

    if len(species_list) > 1:
        click.echo("\nWARNING: Additional high-confidence species were found in the input data:\n")

        for species in species_list[1:]:
            click.echo(species)

    if species.name == "Unknown":  # A species could not be determined.
        click.echo("\nWARNING: A species could not be determined with high confidence from the input data.")

    click.echo("")  # Blank line


def report_strategy(strategy):
    """
    Reports the assembly strategy that will be used to output.

    ARGUMENTS
        strategy (AssemblyStrategy): the assembly strategy that will be used for assembling

    POST
        The assembly strategy will be written to output.
    """

    click.echo(strategy.report)

    if not strategy.proceed:
        click.echo("The assembly was unable to proceed.\n")


def report_contamination(evaluation):
    """
    Reports observed contamination to output.

    ARGUMENTS
        evaluation (Evaluation): an evaluation of observed contamination

    POST
        The evaluation of observed contamination will be written to output.
    """

    click.echo(evaluation.report)

    if not evaluation.success:
        click.echo("The assembly was unable to proceed.\n")


@click.command('assemble',
               short_help='Assemble reads.')
@click.argument('forward', required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('reverse', required=False,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-o', '--output_dir', required=True,
              type=click.Path(exists=False, file_okay=False,
                              dir_okay=True, writable=True))
@click.option('--force', is_flag=True)
@click.pass_context
def cli(ctx, forward, reverse, output_dir, force):

    # Make output directory:
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    reads = Reads(forward, reverse)

    # Validate FASTQ inputs:
    valid_fastq = are_valid_fastq(reads)
    report_valid_fastq(valid_fastq)

    if not valid_fastq and not force:
        return

    # Identify sequencing platform:
    platform_identifier = PlatformIdentifier(reads)
    platform = platform_identifier.identify()
    report_platform(platform)

    # Filter reads:
    read_filterer = ReadFilterer(reads, output_dir)
    filtered_reads = read_filterer.filter_reads()

    forward_filtered = filtered_reads.forward
    reverse_filtered = filtered_reads.reverse
    read_quality = read_filterer.summarize_quality()

    # Estimate species
    species_estimator = SpeciesEstimator([forward_filtered, reverse_filtered], output_dir)
    species_list = species_estimator.estimate_major_species()
    species = species_list[0]
    report_species(species_list)

    # Determine a fast assembly strategy:
    expert = ExpertSystem(platform, species, forward_filtered, reverse_filtered, output_dir)
    fast_strategy = expert.create_fast_assembly_strategy(read_quality)
    report_strategy(fast_strategy)

    if not fast_strategy.proceed and not force:
        return

    # Perform a fast assembly:
    assembler = fast_strategy.assembler
    output = assembler.assemble()
    click.echo(output)

    # Check for contamination at the contig level:
    contamination_handler = ContaminationHandler(species, assembler.contigs_filename, output_dir)
    evaluation = contamination_handler.estimate_contamination()
    report_contamination(evaluation)

    if not evaluation.success and not force:
        return

    # Evaluate fast assembly:
    assembly_evaluator = AssemblyEvaluator(assembler.contigs_filename, output_dir)
    fast_assembly_quality = assembly_evaluator.evaluate()

    # Slow assembly:
    assembly_database = AssemblyDatabase(DATABASE_PATH)
    slow_strategy = expert.create_full_assembly_strategy(fast_assembly_quality, assembly_database)
    report_strategy(slow_strategy)

    if not slow_strategy.proceed and not force:
        return

    click.echo("Performing full assembly.")
    assembler = slow_strategy.assembler
    output = assembler.assemble()
    click.echo(output)

    # Evaluate slow assembly
    assembly_evaluator = AssemblyEvaluator(assembler.contigs_filename, output_dir)
    final_assembly_quality = assembly_evaluator.evaluate()
    evaluation = evaluate_assembly(species, final_assembly_quality, assembly_database)
    click.echo(evaluation.report)

    # Compare fast and slow assemblies:
    report = compare_assemblies(fast_assembly_quality, final_assembly_quality)
    click.echo(report)

    # Write CSV assembly statistics summary:
    assembly_statistics_writer = AssemblyStatisticsWriter(output_dir)
    assembly_statistics_writer.write([fast_strategy.assembler.name, slow_strategy.assembler.name],
                                     [fast_assembly_quality, final_assembly_quality])

    # Move final assembled contigs to the main level of the output directory and rename it.
    contigs_filename = assembler.get_contigs_filename()
    contigs_new_filename = os.path.join(output_dir, "contigs.fasta")
    os.rename(contigs_filename, contigs_new_filename)  # moves and renames

    click.echo("Complete.\n")
