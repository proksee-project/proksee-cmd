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
from proksee.parser.read_quality_parser import parse_read_quality_from_fastp
from proksee.species_estimator import SpeciesEstimator
from proksee.utilities import FastqCheck
from proksee.platform_identify import PlatformIdentify
from proksee.read_filterer import ReadFilterer
from proksee.expert_system import ExpertSystem
from proksee.writer.assembly_statistics_writer import AssemblyStatisticsWriter

DATABASE_PATH = os.path.join(Path(__file__).parent.parent.parent.absolute(), "database",
                             "database.csv")


def check_valid_files(forward, reverse):
    """
    Checks the FASTQ files to see if they are valid FASTQ-format files.

    PARAMETERS
        forward (str): the file location of the forward reads
        reverse (str): the file location of the reverse reads; may be NULL

    RETURNS
        valid (bool): whether or not the both (non-NULL) FASTQ files are valid FASTQ-format files
    """

    fastq_check = FastqCheck(forward, reverse)
    valid = fastq_check.fastq_input_check()

    return valid


def identify_platform(forward, reverse):
    """
    Attempts to identify the sequencing platform used to generate the passed sequencing reads.

    PARAMETERS
        forward (str): the file location of the forward reads
        reverse (str): the file location of the reverse reads; may be NULL

    RETURNS
        platform (str): the estimated sequencing platform
    """

    platform_identify = PlatformIdentify(forward, reverse)
    platform = platform_identify.identify_platform()

    return platform


def filter_reads(forward, reverse, output_directory):
    """
    Filters the reads in order to improve the quality of the reads.

    PARAMETERS
        forward (str): the file location of the forward reads
        reverse (str): the file location of the reverse reads; may be NULL
        output_directory (str): the output directory to write forward and reverse filtered reads

    RETURNS
        forward_filtered (str): the file location of the filtered forward reads
        reverse_filtered (str): the file location of the filtered reverse reads
    """

    read_filterer = ReadFilterer(forward, reverse, output_directory)
    read_filterer.filter_read()

    forward_filtered = read_filterer.forward_filtered
    reverse_filtered = read_filterer.reverse_filtered

    return forward_filtered, reverse_filtered


@click.command('assemble',
               short_help='Assemble reads.')
@click.argument('forward', required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('reverse', required=False,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-o', '--output_dir', required=True,
              type=click.Path(exists=False, file_okay=False,
                              dir_okay=True, writable=True))
@click.pass_context
def cli(ctx, forward, reverse, output_dir):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    valid = check_valid_files(forward, reverse)

    if not valid:
        output_string = 'Either one or both of forward/reverse reads are invalid fastq files..exiting..'
        raise click.UsageError(output_string)

    output_string = 'Read/s is/are valid fastq files..proceeding..'
    click.echo(output_string)

    platform = identify_platform(forward, reverse)
    click.echo(platform)

    # Step 3: Quality Check
    # Pass forward and reverse datasets to read filtering class
    # (with default filters)
    (forward_filtered, reverse_filtered) = filter_reads()

    # TODO: Refactor this better!
    json_file = os.path.join(output_dir, "fastp.json")
    read_quality = parse_read_quality_from_fastp(json_file)

    click.echo("Filtered sequencing reads.\n")

    # Step 4: Organism Detection
    # Pass forward and reverse filtered reads to organism detection class
    # and return most frequently occurring reference genome

    species_estimator = SpeciesEstimator([forward_filtered, reverse_filtered], output_dir)
    species_list = species_estimator.estimate_major_species()

    species = species_list[0]
    click.echo("SPECIES: " + str(species))

    if len(species_list) > 1:
        click.echo("\nWARNING: Additional high-confidence species were found in the input data:\n")

        for species in species_list[1:]:
            click.echo(species)

    if species.name == "Unknown":  # A species could not be determined.
        click.echo("\nWARNING: A species could not be determined with high confidence from the input data.")

    click.echo("")  # Blank line

    # Evaluate reads to determine a fast assembly strategy.
    expert = ExpertSystem(platform, species_list[0], forward_filtered, reverse_filtered, output_dir)
    fast_strategy = expert.create_fast_assembly_strategy(read_quality)
    click.echo(fast_strategy.report)

    if not fast_strategy.proceed:
        click.echo("The assembly was unable to proceed.\n")
        return

    # Step 5: Perform a fast assembly.
    assembler = fast_strategy.assembler
    output = assembler.assemble()
    click.echo(output)

    # Check for contamination at the contig level
    contamination_handler = ContaminationHandler(species, assembler.contigs_filename, output_dir)
    evaluation = contamination_handler.estimate_contamination()

    click.echo(evaluation.report)

    if not evaluation.success:
        click.echo("The assembly was unable to proceed.\n")
        return

    # Step 6: Evaluate Assembly
    assembly_evaluator = AssemblyEvaluator(assembler.contigs_filename, output_dir)

    try:
        fast_assembly_quality = assembly_evaluator.evaluate()

    except Exception:
        raise click.UsageError("Encountered an error when evaluating the assembly.")

    # Step 7: Slow Assembly
    assembly_database = AssemblyDatabase(DATABASE_PATH)

    slow_strategy = expert.create_full_assembly_strategy(fast_assembly_quality, assembly_database)
    click.echo(slow_strategy.report)

    if not slow_strategy.proceed:
        click.echo("The assembly was unable to proceed.\n")
        return

    click.echo("Performing full assembly.")
    assembler = slow_strategy.assembler

    try:
        output = assembler.assemble()
        click.echo(output)

    except Exception:
        raise click.UsageError("Encountered an error when assembling the reads.")

    # Step 6: Evaluate Assembly
    assembly_evaluator = AssemblyEvaluator(assembler.contigs_filename, output_dir)

    try:
        final_assembly_quality = assembly_evaluator.evaluate()

    except Exception:
        raise click.UsageError("Encountered an error when evaluating the assembly.")

    evaluation = evaluate_assembly(species, final_assembly_quality, assembly_database)
    click.echo(evaluation.report)

    # Compare assemblies:
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
