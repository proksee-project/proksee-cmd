"""
Copyright Government of Canada 2020

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

from proksee.pipelines.annotate import annotate
from proksee.resource_specification import ResourceSpecification


@click.command('annotate',
               short_help='Annotate contigs.')
@click.argument('contigs', required=True,
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-o', '--output', required=True,
              type=click.Path(exists=False, file_okay=False,
                              dir_okay=True, writable=True))
@click.option('-t', '--threads', required=False, default=4,
              help="Specifies the number of threads programs in the pipeline should use. The default is 4.")
@click.option('-m', '--memory', required=False, default=4,
              help="Specifies the amount of memory in gigabytes programs in the pipeline should use. The default is 4")
@click.pass_context
def cli(ctx, contigs, output, threads, memory):

    resource_specification = ResourceSpecification(threads, memory)
    annotate(contigs, output, resource_specification)
