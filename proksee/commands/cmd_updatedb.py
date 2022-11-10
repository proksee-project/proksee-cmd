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
import subprocess
import os
import urllib
import urllib.error
import urllib.request

import proksee.config as config

from pathlib import Path

MASH_DATABASE_URL = "https://gembox.cbcb.umd.edu/mash/refseq.genomes.k21s1000.msh"
MASH_DATABASE_FILENAME = "refseq.genomes.k21s1000.msh"

DEFAULT_DATABASE_DIRECTORY = os.path.join(Path(__file__).parent.parent.absolute(), "database")


@click.command('updatedb',
               short_help='Attempts to update the databases used by Proksee.')
@click.option('-d', '--directory', required=False, default=DEFAULT_DATABASE_DIRECTORY,
              help='The directory to place the database files.')
@click.pass_context
def cli(ctx, directory):
    update(directory)


def update(directory):
    """
    The main control flow of the program that attempts to update the Proksee databases.

    ARGUMENTS:
        directory (string): the directory to place the Mash database files

    POST:
        The Proksee database files will be updated if necessary.
    """

    try:
        url_request = urllib.request.Request(MASH_DATABASE_URL, method='HEAD')
        url_response = urllib.request.urlopen(url_request)
        file_size = int(url_response.headers['Content-Length'])

    except (urllib.error.HTTPError, urllib.error.URLError,
            urllib.error.ContentTooShortError):
        raise urllib.error.URLError("Could not get header for Mash sketch " +
                                    "file file from {}.".format(MASH_DATABASE_URL))

    except TimeoutError:
        raise TimeoutError("Could not fetch header for Mash sketch " +
                           "file from {} before timeout.".format(MASH_DATABASE_URL))

    # Make database directory:
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        os.mkdir(directory)

    mash_database_path = os.path.join(directory, MASH_DATABASE_FILENAME)
    config.update(config.MASH_PATH, mash_database_path)

    if not os.path.isfile(mash_database_path) or \
            file_size != os.path.getsize(mash_database_path):

        click.echo("Downloading database...")

        command = "wget -O " + str(mash_database_path) + " " + MASH_DATABASE_URL + " --progress=dot:giga"

        try:
            subprocess.check_call(command, shell=True)

        except subprocess.CalledProcessError:
            click.echo("Encountered an error when downloading the database.")

    else:
        click.echo("Database already downloaded!")

    click.echo("Complete.")
