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

from proksee.assembly_evaluator import AssemblyEvaluator


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

    # Step 1: Check if the forward and reverse reads are valid fastq files
    # Pass the forward and reverse data to fastq check class and check
    fastq_check = FastqCheck(forward, reverse)
    fastq_string, fastq_bool = fastq_check.fastq_input_check()
    if not fastq_bool:
        '''Program exits if fastq status is False'''
        raise click.UsageError(fastq_string)
    else:
        click.echo(fastq_string)

        # Step 2: Platform detection
        # Pass forward and reverse datasets to platform detection class and
        # output sequencing platform/s
        platform_identify = PlatformIdentify(forward, reverse)
        platform = platform_identify.identify_platform()
        click.echo(platform)

        # Step 3: Quality Check
        # Pass forward and reverse datasets to read filtering class
        # (with default filters)
        read_filtering = ReadFiltering(forward, reverse, output_dir)
        filtering = read_filtering.filter_read()
        click.echo(filtering)

        '''The next steps are executed on filtered read/s'''
        forward_filtered = os.path.join(output_dir, 'fwd_filtered.fastq')
        if reverse is None:
            reverse_filtered = None
        else:
            reverse_filtered = os.path.join(output_dir, 'rev_filtered.fastq')

        # Step 4: Organism Detection
        # Pass forward and reverse filtered reads to organism detection class
        # and return most frequently occuring reference genome
        organism_identify = OrganismDetection(forward_filtered, reverse_filtered, output_dir)
        try:
            major_organism = organism_identify.major_organism()
            click.echo(major_organism)

            '''Catch exception if input reads are too short for reference genome estimation'''
        except Exception:
            raise click.UsageError('encountered errors running refseq_masher, \
                this may have been caused by too small of file reads')

        # Step 5: Assembly (Only skesa for now)
        # Pass forward and reverse filtered reads to assembler class
        # and return a finished genome assembly within output path
        assembler = Assembler(forward_filtered, reverse_filtered, output_dir)
        try:
            assembly = assembler.perform_assembly()
            print(assembly)

            '''Catch exception if input reads are short for skesa kmer estimation'''
        except Exception:
            raise click.UsageError('encountered errors running skesa, \
                this may have been caused by too small of file reads')

        # Step 6: Evaluate Assembly
        assembly_evaluator = AssemblyEvaluator(assembler.contigs_filename, output_dir)

        try:
            report = assembly_evaluator.evaluate()
            print(report)

        except Exception:
            raise click.UsageError("Encountered an error when evaluating the assembly.")
