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

    #raise click.UsageError("command not yet implemented")

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Step 1: Platform detection
    # Pass forward and reverse datasets to platform detection module and ensure that both files are of the same platform
    file_dicn = platform_identify.fastq_extn_check(forward, reverse)
    output_dicn = platform_identify.platform_output(file_dicn)
    complete1 = platform_identify.output_write(output_dicn, output_dir)
    sys.stdout.write(complete1)
    # Step 2: Quality Check
    # Pass forward and reverse datasets to quality check module and calculate quality statistics

    # Step 3: Organism Detection
    # Pass forward and reverse datasets to organism detection module and return the dominate genus and species

    # Step 4: Assembly (Only skesa for now)
    # Pass forward and reverse datasets to assembly module and return a path to the results or paths to specific files
