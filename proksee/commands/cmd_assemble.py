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

from proksee.assembly_evaluator import AssemblyEvaluator
from proksee.assembly_database import AssemblyDatabase
from proksee.utilities import FastqCheck
from proksee.platform_identify import PlatformIdentify
from proksee.read_filterer import ReadFilterer
from proksee.organism_detection import OrganismDetection
from proksee.expert_system import ExpertSystem

DATABASE_PATH = os.path.join(Path(__file__).parent.parent.parent.absolute(), "tests", "data",
                             "fake_assembly_data.csv")


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
        read_filterer = ReadFilterer(forward, reverse, output_dir)
        output = read_filterer.filter_read()
        read_quality = read_filterer.summarize_quality()

        click.echo(output)

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
            species_list = organism_identify.major_organism()
            click.echo("Major reference organism is/are {}".format(species_list))

            '''Catch exception if input reads are too short for reference genome estimation'''
        except Exception:
            raise click.UsageError('encountered errors running refseq_masher, \
                this may have been caused by too small of file reads')

        # Evaluate reads to determine a fast assembly strategy.
        expert = ExpertSystem(platform, species_list[0], forward_filtered, reverse_filtered, output_dir)
        strategy = expert.create_fast_assembly_strategy(read_quality)
        click.echo(strategy.report)

        if not strategy.proceed:
            click.echo("The assembly was unable to proceed.")
            return

        # Step 5: Perform a fast assembly.
        assembler = strategy.assembler

        try:
            assembly = assembler.assemble()
            print(assembly)

            '''Catch exception if input reads are short for skesa kmer estimation'''
        except Exception:
            raise click.UsageError('encountered errors running skesa, \
                this may have been caused by too small of file reads')

        # Step 6: Evaluate Assembly
        assembly_evaluator = AssemblyEvaluator(assembler.contigs_filename, output_dir)

        try:
            assembly_quality = assembly_evaluator.evaluate()

        except Exception:
            raise click.UsageError("Encountered an error when evaluating the assembly.")

        # Step 7: Slow Assembly
        assembly_database = AssemblyDatabase(DATABASE_PATH)

        strategy = expert.create_full_assembly_strategy(assembly_quality, assembly_database)
        click.echo(strategy.report)

        if not strategy.proceed:
            click.echo("The assembly was unable to proceed.")
            return

        click.echo("Performing full assembly.")
        assembler = strategy.assembler
        assembler.assemble()

        click.echo("Complete.")
