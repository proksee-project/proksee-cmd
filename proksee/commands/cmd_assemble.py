import click
import os
import sys

# import platform detection
from proksee import platform_identify

# import quality module
from proksee import read_quality

# import organism detection
from proksee import organism_detection

# import assembler
from proksee import assembler

@click.command('assemble',
               short_help='Assemble reads.')
@click.argument('forward', required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('reverse', required=False,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-o', '--output_dir', required=True,
              type=click.Path(exists=False, file_okay=False, dir_okay=True, writable=True))
@click.pass_context
def cli(ctx, forward, reverse, output_dir):

    raise click.UsageError("command not yet implemented")

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Step 1: Platform detection
    # Pass forward and reverse datasets to platform detection module and ensure that both files are of the same platform
    file_dicn = platform_identify.fastq_extn_check(forward, reverse)
    platform_dicn = platform_identify.platform_output(file_dicn)
    print(platform_dicn)
    sys.stdout.write('Platform identification complete')


    # Step 2: Quality Check
    # Pass forward and reverse datasets to quality check module and calculate quality statistics
    fastp_output = os.path.join(output_dir, fastp_output_file)
    fastp_log = os.path.join(output_dir, fastp_log_file)
    fastp_string = read_quality.fastp_string(forward, reverse, fastp_output)
    read_quality.fastp_func(fastp_string, fastp_output, fastp_log)
    sys.stdout.write('Read quality assessment complete')

    # Step 3: Organism Detection
    # Pass forward and reverse datasets to organism detection module and return the dominate genus and species
    refseq_output = os.path.join(output_dir, refseq_output_file)
    refseq_log = os.path.join(output_dir, refseq_log_file)
    refseq_string = organism_detection.refseq_masher_string(forward, reverse)
    organism_detection.refseq_masher_func(refseq_string, refseq_output, refseq_log)
    sys.stdout.write('Organism detection complete')

    # Step 4: Assembly (Only skesa for now)
    # Pass forward and reverse datasets to assembly module and return a path to the results or paths to specific files
    skesa_output = os.path.join(output_dir, skesa_output_file)
    skesa_log = os.path.join(output_dir, skesa_log_file)
    skesa_string = assembler.skesa_string(forward, reverse)
    assembler.skesa_func(skesa_string, skesa_output, skesa_log)
    sys.stdout.write('Assembler (skesa) complete')