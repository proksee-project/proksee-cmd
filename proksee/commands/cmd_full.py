"""
Copyright Government of Canada 2022

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

from proksee import utilities
from proksee.pipelines.assemble import assemble
from proksee.pipelines.annotate import annotate
from proksee.resource_specification import ResourceSpecification
from proksee import config as config
from proksee.reads import Reads


@click.command('full',
               short_help='Assembles reads and annotates the resulting contigs.')
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
@click.option('-t', '--threads', required=False, default=4,
              help="Specifies the number of threads programs in the pipeline should use. The default is 4.")
@click.option('-m', '--memory', required=False, default=4,
              help="Specifies the amount of memory in gigabytes programs in the pipeline should use. The default is 4")
@click.pass_context
def cli(ctx, forward, reverse, output, force, species, platform, threads, memory):

    # Check Mash database is installed:
    mash_database_path = config.get(config.MASH_PATH)

    if not os.path.isfile(mash_database_path):
        print("Please run 'proksee updatedb' to install the databases!")
        return

    print(utilities.build_version_message())

    reads = Reads(forward, reverse)
    resource_specification = ResourceSpecification(threads, memory)
    contigs_filename = assemble(reads, output, force, config.DATABASE_PATH, mash_database_path,
                                resource_specification, config.ID_MAPPING_FILENAME, species, platform)
    annotate(contigs_filename, output, resource_specification)
