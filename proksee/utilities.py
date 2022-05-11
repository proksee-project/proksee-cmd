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

from proksee import __version__ as version
from proksee.database.version import MODEL_VERSION, NORM_DATABASE_VERSION

from proksee.species import Species
from proksee.species_estimator import SpeciesEstimator


def determine_species(input_filenames, assembly_database, output_directory, mash_database_filename,
                      id_mapping_filename, species_name=None):
    """
    Attempts to determine the species in the input (reads or contigs).

    ARGUMENTS:
        input_filenames (List(string)): the inputs (filenames) from which to determine the species from
        assembly_database (AssemblyDatabase): the assembly database
        output_directory (string): the location of the output directory for placing temporary output
        mash_database_filename (string): the filename of the Mash sketch (database) file
        id_mapping_filename (string): the filename of the NCBI ID-to-taxonomy mapping file
        species_name (string): optional; the scientific name of the species

    RETURNS:
        species_list (List(Species)): a list of major species estimated to be present in the input
    """

    species_list = None

    if species_name:
        if assembly_database.contains(species_name):
            click.echo("\nThe species '" + str(species_name) + "' was recognized.")
            species_list = [Species(species_name, 1.0)]

        else:
            click.echo("\nThe species name '" + str(species_name) + "' is unrecognized.")

    if species_list is None:
        click.echo("\nAttempting to identify the species from the input.")

        species_estimator = SpeciesEstimator(input_filenames, output_directory, mash_database_filename,
                                             id_mapping_filename)
        species_list = species_estimator.estimate_major_species()

    return species_list


def build_version_message():
    """
    Builds a message containing the version numbers of the software and databases.

    RETURNS:
        message (String): a message containing the version numbers of the software and databases.
    """

    message = ('Proksee Version'
               + '\n  Software: {}'.format(version)
               + '\n  Model: {}'.format(MODEL_VERSION)
               + '\n  Database: {}'.format(NORM_DATABASE_VERSION)
               + '\n')

    return message
