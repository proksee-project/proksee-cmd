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
import time

from proksee import __version__ as version
from proksee.database.version import MODEL_VERSION, NORM_DATABASE_VERSION

from proksee.species import Species
from proksee.species_estimator import SpeciesEstimator

from enum import Enum


class InputType(Enum):
    READS = "Reads"
    ASSEMBLY = "Assembly"


def get_time():
    """
    Returns the current time as a formatted string.
    """

    return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())


def determine_major_species(input_filenames, assembly_database, output_directory, mash_database_filename,
                            id_mapping_filename, input_type, species_name=None):
    """
    Attempts to determine the species in the input (reads or assembly).

    ARGUMENTS:
        input_filenames (List(string)): the inputs (filenames) from which to determine the species from
        assembly_database (AssemblyDatabase): the assembly database
        output_directory (string): the location of the output directory for placing temporary output
        mash_database_filename (string): the filename of the Mash sketch (database) file
        id_mapping_filename (string): the filename of the NCBI ID-to-taxonomy mapping file
        input_type (InputType): InputType.READS or InputType.ASSEMBLY
        species_name (string): optional; the scientific name of the species

    RETURNS:
        species_list (List(Species)): a list of major species estimated to be present in the input
    """

    species_list = None

    if species_name:
        if assembly_database.contains(species_name):
            click.echo("\n" + get_time())
            click.echo("The species '" + str(species_name) + "' was recognized.")
            species_list = [Species(species_name, 1.0)]

        else:
            click.echo("\n" + get_time())
            click.echo("The species name '" + str(species_name) + "' is unrecognized.")

    if species_list is None:
        click.echo("\n" + get_time())
        click.echo("Attempting to identify the species from the input.")

        species_estimator = SpeciesEstimator(input_filenames, output_directory, mash_database_filename,
                                             id_mapping_filename)
        if input_type == InputType.READS:
            click.echo("\nAttempting to identify the species from the reads.")
            species_list = species_estimator.estimate_major_species_from_reads()

        elif input_type == InputType.ASSEMBLY:
            click.echo("\nAttempting to identify the species from the assembly.")
            species_list = species_estimator.estimate_major_species_from_assembly()

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
               + '\n  Database: {}'.format(NORM_DATABASE_VERSION))

    return message


def filter_spades_contigs_by_length(input_file_location, output_file_location, minimum_contig_length):
    """
    Filters a SPAdes-generated assembly by creating a copy of the contigs file that contains only contigs with a length
    greater than specified.

    POST:
        A file named according to the passed output_file_location will be created and contain only SPAdes-generated
        assembly contigs with lengths >= minimum_contig_length.
    """

    LENGTH_POSITION = 3  # The SPAdes FASTA record headers look like: ">NODE_1_length_7819_cov_4.681350"

    output_contig_file = open(output_file_location, "w")

    with open(input_file_location) as input_contigs_file:
        for line in input_contigs_file.readlines():
            # All the SPAdes contigs are sorted by length.
            # If we have a new FASTA record and the length isn't long enough, stop writing everything.
            if line.startswith(">") and not int(line.split("_")[LENGTH_POSITION]) >= minimum_contig_length:
                output_contig_file.close()
                break
            # Otherwise, keep writing.
            else:
                output_contig_file.write(line)

    output_contig_file.close()
