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

from pathlib import Path

MASH_DATABASE = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                             "refseq.genomes.k21s1000.msh")
MASH_DATABASE_URL = "https://gembox.cbcb.umd.edu/mash/refseq.genomes.k21s1000.msh"

@click.command('updatedb',
               short_help='Attempts to update the databases used by Proksee.')
@click.pass_context
def cli(ctx):
    update()


def update(mash_database_filename=MASH_DATABASE):
    """
    The main control flow of the program that attempts to update the Proksee databases.

    ARGUMENTS:
        mash_database_filename (string): optional; the filename of the Mash database

    POST:
        The Proksee databases will be updated if necessary.
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


    if not os.path.isfile(mash_database_filename) or \
            file_size != os.path.getsize(MASH_DATABASE):

        click.echo("Downloading database...")

        command = "wget -O " + MASH_DATABASE + " " + MASH_DATABASE_URL

        try:
            subprocess.check_call(command, shell=True)

        except subprocess.CalledProcessError:
            click.echo("Encountered an error when downloading the database.")

    else:
        click.echo("Database already downloaded!")

    click.echo("Complete.")
