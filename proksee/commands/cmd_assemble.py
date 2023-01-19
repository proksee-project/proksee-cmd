"""
Copyright Government of Canada 2020-2022

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
from shutil import rmtree

from proksee import utilities
from proksee.utilities import InputType
from proksee.utilities import get_time


from proksee.assembly_database import AssemblyDatabase
from proksee.assembly_measurer import AssemblyMeasurer
from proksee.contamination_handler import ContaminationHandler
from proksee.heuristic_evaluator import compare_assemblies
from proksee.species_assembly_evaluator import SpeciesAssemblyEvaluator
from proksee.ncbi_assembly_evaluator import NCBIAssemblyEvaluator
from proksee.input_verification import are_valid_fastq
from proksee.machine_learning_evaluator import MachineLearningEvaluator
from proksee.reads import Reads
from proksee.platform_identify import PlatformIdentifier, identify_name, Platform
from proksee.read_filterer import ReadFilterer
from proksee.expert_system import ExpertSystem
from proksee.writer.assembly_statistics_writer import AssemblyStatisticsWriter
from proksee import config as config
from proksee.species_estimator import SpeciesEstimator
from proksee.skesa_assembler import SkesaAssembler
from proksee.spades_assembler import SpadesAssembler
from proksee.resource_specification import ResourceSpecification

DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                             "refseq_short.csv")
ID_MAPPING_FILENAME = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                                   "mash_id_mapping.tab.gz")


def report_valid_fastq(valid):
    """
    Reports to output whether or not the reads appear to be in a valid FASTQ file format.

    ARGUMENTS
        valid (bool): whether or not the reads appear to be in FASTQ format

    POST
        A statement reporting whether or not the reads appear to be in a valid FASTQ file format will be written to the
        program's output.
    """

    output = get_time() + "\n"

    if not valid:
        output += "One or both of the reads are not in FASTQ format."

    else:
        output += "The reads appear to be formatted correctly."

    click.echo(output)


def report_platform(platform):
    """
    Reports the sequencing platform to output.

    ARGUMENTS
        platform (Platform (Enum)): the sequencing platform to report

    POST
        A statement reporting the sequencing platform will be written to output.
    """

    output = "Sequencing Platform: " + str(platform.value)

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
    click.echo("\n" + get_time())
    click.echo("SPECIES: " + str(species))

    if len(species_list) > 1:
        click.echo("\nWARNING: Additional high-confidence species were found in the input data:\n")

        for species in species_list[1:min(5, len(species_list))]:
            click.echo(species)

    if species.name == "Unknown":  # A species could not be determined.
        click.echo("\nWARNING: A species could not be determined with high confidence from the input data.")


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
        click.echo("\nThe assembly was unable to proceed.")


def report_contamination(evaluation):
    """
    Reports observed contamination to output.

    ARGUMENTS
        evaluation (Evaluation): an evaluation of observed contamination

    POST
        The evaluation of observed contamination will be written to output.
    """

    click.echo("\n" + get_time())
    click.echo(evaluation.report)

    if not evaluation.success:
        click.echo("\nThe assembly was unable to proceed.")


def determine_platform(reads, platform_name=None):
    """
    Attempts to determine the sequencing platform used to generate the reads.

    ARGUMENTS:
        reads (Reads): the reads generated by the sequencing platform
        platform_name (string): optional; the name of the sequencing platform

    RETURNS:
        platform (Platform): the estimated sequencing platform
    """

    platform = Platform.UNIDENTIFIABLE

    if platform_name:
        platform = identify_name(platform_name)

        if platform is Platform.UNIDENTIFIABLE:
            click.echo("\n" + get_time())
            click.echo("The platform name '" + str(platform_name) + "' is unrecognized.")
            click.echo("Please see the help message for valid platform names.")

        else:
            click.echo("\n" + get_time())
            click.echo("The platform name '" + str(platform_name) + "' was recognized.")

    if platform is Platform.UNIDENTIFIABLE:
        click.echo("\n" + get_time())
        click.echo("Attempting to identify the sequencing platform from the reads.")

        platform_identifier = PlatformIdentifier(reads)
        platform = platform_identifier.identify()

    return platform


@click.command('assemble',
               short_help='Assemble reads.')
@click.argument('forward', required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('reverse', required=False,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-o', '--output', required=True,
              type=click.Path(exists=False, file_okay=False,
                              dir_okay=True, writable=True))
@click.option('--force', is_flag=True,
              help="This will force the assembler to proceed when the assembly appears to be poor.")
@click.option('-s', '--species', required=False, default=None,
              help="The species to assemble. This will override species estimation. Must be spelled correctly.")
@click.option('-p', '--platform', required=False, default=None,
              help="The sequencing platform used to generate the reads. 'Illumina', 'Ion Torrent', or 'Pac Bio'.")
@click.option('--min-contig-length', required=False, default=1000, type=click.IntRange(min=0, max=None),
              help="The minimum contig length to include in analysis and output. The default is 1000.")
@click.option('-t', '--threads', required=False, default=4, type=click.IntRange(min=0, max=None),
              help="Specifies the number of threads programs in the pipeline should use. The default is 4.")
@click.option('-m', '--memory', required=False, default=4, type=click.IntRange(min=0, max=None),
              help="Specifies the amount of memory in gigabytes programs in the pipeline should use. The default is 4")
@click.pass_context
def cli(ctx, forward, reverse, output, force, species, platform, min_contig_length, threads, memory):

    # Check Mash database is installed:
    mash_database_path = config.get(config.MASH_PATH)

    if not os.path.isfile(mash_database_path):
        print("Please run 'proksee updatedb' to install the databases!")
        return

    reads = Reads(forward, reverse)
    resource_specification = ResourceSpecification(threads, memory)
    assemble(reads, output, force, mash_database_path, resource_specification, species, platform, min_contig_length)
    cleanup(output)


def cleanup(output_directory):
    """
    Cleans up temporary files in the output directory.

    ARGUMENTS:
        output_directory (string): the location of the program output

    POST:
        The output directory will have all temporary program files deleted.
    """

    # Temporary FASTA directory used in contamination detection:
    fasta_directory = os.path.join(output_directory, ContaminationHandler.FASTA_DIRECTORY)

    if os.path.isdir(fasta_directory):
        rmtree(fasta_directory)

    # Read filtering logfile (i.e. fastp.log):
    filterer_logfile_path = os.path.join(output_directory, ReadFilterer.LOGFILE_FILENAME)

    if os.path.isfile(filterer_logfile_path):
        os.remove(filterer_logfile_path)

    # Forward and reverse filtered read files:
    fwd_filtered_path = os.path.join(output_directory, ReadFilterer.FWD_FILTERED_FILENAME)
    rev_filtered_path = os.path.join(output_directory, ReadFilterer.REV_FILTERED_FILENAME)

    if os.path.isfile(fwd_filtered_path):
        os.remove(fwd_filtered_path)

    if os.path.isfile(rev_filtered_path):
        os.remove(rev_filtered_path)

    # Species estimation output (i.e. mash.o):
    species_estimation_path = os.path.join(output_directory, SpeciesEstimator.OUTPUT_FILENAME)

    if os.path.isfile(species_estimation_path):
        os.remove(species_estimation_path)

    # Assembly quality measurer temporary files (i.e. quast.out and quast.err)
    assembly_measurer_output_path = os.path.join(output_directory, AssemblyMeasurer.OUTPUT_FILENAME)
    assembly_measurer_error_path = os.path.join(output_directory, AssemblyMeasurer.ERROR_FILENAME)

    if os.path.isfile(assembly_measurer_output_path):
        os.remove(assembly_measurer_output_path)

    if os.path.isfile(assembly_measurer_error_path):
        os.remove(assembly_measurer_error_path)

    # Assembly output directories:
    skesa_directory = os.path.join(output_directory, SkesaAssembler.DIRECTORY_NAME)
    spades_directory = os.path.join(output_directory, SpadesAssembler.DIRECTORY_NAME)

    if os.path.isdir(skesa_directory):
        rmtree(skesa_directory)

    if os.path.isdir(spades_directory):
        rmtree(spades_directory)


def assemble(reads, output_directory, force, mash_database_path, resource_specification,
             species_name=None, platform_name=None, minimum_contig_length=1000,
             id_mapping_filename=ID_MAPPING_FILENAME):
    """
    The main control flow of the program that assembles reads.

    ARGUMENTS:
        reads (Reads): the reads to assemble
        output_directory (string): the location to place all program output and temporary files
        force (bool): whether or not to force the assembly to continue, even when it's evaluated as being poor
        mash_database_path (string): optional; the file path of the Mash database
        resource_specification (ResourceSpecification): the resources that sub-programs should use
        species_name (string): optional; the name of the species being assembled
        platform_name (string): optional; the name of the sequencing platform that generated the reads
        minimum_contig_length (int): optional; the minimum contig length to use for assembly and analysis
        id_mapping_filename (string) optional; the name of the NCBI ID to taxonomy mapping database file

    POST:
        The passed reads will be assembled in the output directory if successful, or a message explaning why assembly
        could not continue will be written to standard output.
    """

    click.echo("\n" + get_time())
    click.echo(utilities.build_version_message() + "\n")

    # Make output directory:
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    # Validate FASTQ inputs:
    valid_fastq = are_valid_fastq(reads)
    report_valid_fastq(valid_fastq)

    if not valid_fastq and not force:
        return

    platform = determine_platform(reads, platform_name)
    report_platform(platform)

    # Filter reads:
    read_filterer = ReadFilterer(reads, output_directory)
    filtered_reads = read_filterer.filter_reads()
    read_quality = read_filterer.summarize_quality()

    # Species and assembly database:
    assembly_database = AssemblyDatabase(DATABASE_PATH)

    # Estimate species
    filtered_filenames = filtered_reads.get_file_locations()
    species_list = utilities.determine_major_species(filtered_filenames, assembly_database, output_directory,
                                                     mash_database_path, id_mapping_filename, InputType.READS,
                                                     species_name)
    species = species_list[0]
    report_species(species_list)

    # Determine a fast assembly strategy:
    expert = ExpertSystem(platform, species, filtered_reads, output_directory, resource_specification)
    fast_strategy = expert.create_fast_assembly_strategy(read_quality)
    click.echo("\n" + get_time())
    report_strategy(fast_strategy)

    if not fast_strategy.proceed and not force:
        return

    # Perform a fast assembly:
    assembler = fast_strategy.assembler
    output = assembler.assemble()
    click.echo("\n" + get_time())
    click.echo(output)

    # Check for contamination at the contig level:
    contamination_handler = ContaminationHandler(species, assembler.contigs_filename, output_directory,
                                                 mash_database_path, id_mapping_filename)
    evaluation = contamination_handler.estimate_contamination()
    report_contamination(evaluation)

    if not evaluation.success and not force:
        return

    # Measure assembly quality statistics:
    assembly_measurer = AssemblyMeasurer(assembler.contigs_filename, output_directory, minimum_contig_length)
    click.echo("\n" + get_time())
    fast_assembly_quality = assembly_measurer.measure_quality()

    # Machine learning evaluation (fast assembly)
    machine_learning_evaluator = MachineLearningEvaluator(species)
    evaluation = machine_learning_evaluator.evaluate(fast_assembly_quality)

    click.echo("\n" + get_time())
    click.echo(evaluation.report)

    # Expert assembly:
    expert_strategy = expert.create_expert_assembly_strategy(fast_assembly_quality, assembly_database)
    click.echo("\n" + get_time())
    report_strategy(expert_strategy)

    if not expert_strategy.proceed and not force:
        return

    click.echo("\n" + get_time())
    click.echo("Performing expert assembly.")
    assembler = expert_strategy.assembler
    output = assembler.assemble()
    click.echo(output)

    # Measure assembly quality:
    assembly_measurer = AssemblyMeasurer(assembler.contigs_filename, output_directory, minimum_contig_length)
    expert_assembly_quality = assembly_measurer.measure_quality()

    # Machine learning evaluation (expert assembly)
    machine_learning_evaluation = machine_learning_evaluator.evaluate(expert_assembly_quality)
    click.echo("\n" + get_time())
    click.echo(machine_learning_evaluation.report)

    # NCBI RefSeq Exclusion Criteria Evaluation
    click.echo("\n" + get_time())
    click.echo("Comparing the assembly against the NCBI RefSeq exclusion criteria:\n")
    ncbi_evaluator = NCBIAssemblyEvaluator(species, assembly_database)
    ncbi_evaluation = ncbi_evaluator.evaluate_assembly_from_fallback(expert_assembly_quality)
    click.echo(ncbi_evaluation.report)

    # Species-Based Evaluation
    click.echo("\n" + get_time())
    click.echo("Comparing the assembly to similar assemblies of the same species:")
    species_evaluator = SpeciesAssemblyEvaluator(species, assembly_database)
    species_evaluation = species_evaluator.evaluate_assembly_from_database(expert_assembly_quality)
    click.echo(species_evaluation.report)

    # Compare fast and slow assemblies:
    report = compare_assemblies(fast_assembly_quality, expert_assembly_quality)
    click.echo("\n" + get_time())
    click.echo(report)

    # Write CSV assembly statistics summary:
    assembly_statistics_writer = AssemblyStatisticsWriter(output_directory)
    assembly_statistics_writer.write_csv([fast_strategy.assembler.name, expert_strategy.assembler.name],
                                         [fast_assembly_quality, expert_assembly_quality])

    # Write expert assembly information to JSON file:
    assembly_statistics_writer.write_json(platform, species, reads, read_quality, expert_assembly_quality,
                                          species_evaluation, machine_learning_evaluation, ncbi_evaluation,
                                          assembly_database)

    # Move final assembled contigs to the main level of the output directory and rename it:
    contigs_filename = assembler.get_contigs_filename()
    contigs_new_filename = os.path.join(output_directory, "contigs.all.fasta")
    os.rename(contigs_filename, contigs_new_filename)  # moves and renames

    # Filter the assembled contigs by length and save in a new file:
    contigs_filtered_filename = os.path.join(output_directory, "contigs.filtered.fasta")
    utilities.filter_spades_contigs_by_length(contigs_new_filename, contigs_filtered_filename, minimum_contig_length)

    click.echo("\n" + get_time())
    click.echo("Complete.\n")
