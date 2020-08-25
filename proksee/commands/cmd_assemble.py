import click
import os
import sys
import subprocess

# import fastq check
from proksee.utilities import FastqCheck

# import platform detection
from proksee.platform_identify import PlatformIdentify

# import quality module
from proksee.read_quality import ReadFiltering

# import organism detection
from proksee.organism_detection import OrganismDetection

# import assembler
from proksee.assembler import Assembler

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


    # Step 1: Check if the forward and reverse reads are valid fastq files
    # Pass the forward and reverse data to fastq check module and check
    fastq_check = FastqCheck(forward, reverse)
    fastq_string, fastq_bool = fastq_check.fastq_input_check()
    if not fastq_bool:
        sys.exit(fastq_string)
    else:
        print(fastq_string)
        # Step 1: Platform detection
        # Pass forward and reverse datasets to platform detection module and ensure that both files are of the same platform
        platform_identify = PlatformIdentify(forward, reverse)
        platform = platform_identify.identify_platform()
        print(platform)

        # Step 2: Quality Check
        # Pass forward and reverse datasets to quality check module and calculate quality statistics
        read_filtering = ReadFiltering(forward, reverse, output_dir)
        filtering = read_filtering.filter_read()
        print(filtering)

        forward_filtered = os.path.join(output_dir, 'fwd_filtered.fastq')
        if reverse is None:
            reverse_filtered = None
        else:
            reverse_filtered = os.path.join(output_dir, 'rev_filtered.fastq')

        # Step 3: Organism Detection
        # Pass forward and reverse datasets to organism detection module and return the dominate genus and species
        organism_identify = OrganismDetection(forward_filtered, reverse_filtered, \
            output_dir)
        try:
            major_organism = organism_identify.major_organism()
            print(major_organism)
        except subprocess.CalledProcessError:
            print('refseq_masher error: File size too small for creating Mash sketch')

        # Step 4: Assembly (Only skesa for now)
        # Pass forward and reverse datasets to assembly module and return a path to the results or paths to specific files
        assembler = Assembler(forward_filtered, reverse_filtered, output_dir)
        try:
            assembly = assembler.perform_assembly()
            print(assembly)
        except subprocess.CalledProcessError:
            print('Skesa error: Reads too short for selecting minimal kmer length')