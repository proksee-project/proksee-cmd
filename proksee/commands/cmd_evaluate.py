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

from proksee.pipelines.evaluate import evaluate

import proksee.config as config

DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                             "refseq_short.csv")
ID_MAPPING_FILENAME = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                                   "mash_id_mapping.tab.gz")


@click.command('evaluate',
               short_help='Evaluates the quality of an assembly.')
@click.argument('contigs', required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-s', '--species', required=False, default=None,
              help="The species to assemble. This will override species estimation. Must be spelled correctly.")
@click.option('-o', '--output', required=True,
              type=click.Path(exists=False, file_okay=False,
                              dir_okay=True, writable=True))
@click.pass_context
def cli(ctx, contigs, output, species):

    # Check Mash database is installed:
    mash_database_path = config.get(config.MASH_PATH)

    if not os.path.isfile(mash_database_path):
        print("Please run 'proksee updatedb' to install the databases!")
        return

    evaluate(contigs, output, DATABASE_PATH, mash_database_path, ID_MAPPING_FILENAME, species)
