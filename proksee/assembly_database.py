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

import os
import csv


class AssemblyDatabase:
    """
    A class representing a database containing aggregate information about assemblies for different species.

    ATTRIBUTES
        database (dict): a dictionary mapping species to assembly information
        database_filename (str): the filename of the database
    """

    # Constants for different assembly statistics. These are used both to identify position in parsing,
    # and as unique identifiers for dictionaries.
    SPECIES = 0
    COUNT = 1
    N50_05 = 2  # the 0.05 quantile of the N50
    N50_20 = 3  # the 0.20 quantile of the N50
    N50_50 = 4
    N50_80 = 5
    N50_95 = 6
    CONTIG_05 = 7   # the 0.05 quantile of the number of contigs
    CONTIG_20 = 8   # the 0.20 quantile of the number of contigs
    CONTIG_50 = 9
    CONTIG_80 = 10
    CONTIG_95 = 11
    L50_05 = 12   # the 0.05 quantile of the L50
    L50_20 = 13  # the 0.20 quantile of the L50
    L50_50 = 14
    L50_80 = 15
    L50_95 = 16
    LENGTH_05 = 17  # the 0.05 quantile of the assembly length
    LENGTH_20 = 18  # the 0.20 quantile of the assembly length
    LENGTH_50 = 19
    LENGTH_80 = 20
    LENGTH_95 = 21

    # Constants acting as dictionary keys for accessing the database information.
    SPECIES_COUNT = "SPECIES_COUNT"
    N50_QUANTILES = "N50_QUANTILES"
    CONTIGS_QUANTILES = "CONTIGS_QUANTILES"
    L50_QUANTILES = "L50_QUANTILES"
    LENGTH_QUANTILES = "LENGTH_QUANTILES"

    # Thresholds as quantiles:
    LOW_ERROR_QUANTILE = 0.05
    LOW_WARNING_QUANTILE = 0.20
    MEDIAN = 0.50
    HIGH_WARNING_QUANTILE = 0.80
    HIGH_ERROR_QUANTILE = 0.95

    def __init__(self, database_filename):
        """
        Initializes the database.

        PARAMETERS
            database_filename (str): the filename of the assembly database
        """

        self.database = {}
        self.database_filename = database_filename

        if not os.path.exists(database_filename):
            raise FileNotFoundError(str(database_filename) + " not found!")

        self.load()

    def load(self):
        """
        Loads the database.

        POST
            The database will be loaded from file and accessible by this object.
        """

        self.database = {}

        with open(self.database_filename) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            next(reader)  # skip header

            for row in reader:
                species = row[self.SPECIES]

                count = row[self.COUNT]

                n50_quantiles = {}
                contigs_quantiles = {}
                l50_quantiles = {}
                length_quantiles = {}

                n50_quantiles[0.05] = row[self.N50_05]
                n50_quantiles[0.20] = row[self.N50_20]
                n50_quantiles[0.50] = row[self.N50_50]
                n50_quantiles[0.80] = row[self.N50_80]
                n50_quantiles[0.95] = row[self.N50_95]

                contigs_quantiles[0.05] = row[self.CONTIG_05]
                contigs_quantiles[0.20] = row[self.CONTIG_20]
                contigs_quantiles[0.50] = row[self.CONTIG_50]
                contigs_quantiles[0.80] = row[self.CONTIG_80]
                contigs_quantiles[0.95] = row[self.CONTIG_95]

                l50_quantiles[0.05] = row[self.L50_05]
                l50_quantiles[0.20] = row[self.L50_20]
                l50_quantiles[0.50] = row[self.L50_50]
                l50_quantiles[0.80] = row[self.L50_80]
                l50_quantiles[0.95] = row[self.L50_95]

                length_quantiles[0.05] = row[self.LENGTH_05]
                length_quantiles[0.20] = row[self.LENGTH_20]
                length_quantiles[0.50] = row[self.LENGTH_50]
                length_quantiles[0.80] = row[self.LENGTH_80]
                length_quantiles[0.95] = row[self.LENGTH_95]

                information = {
                    self.SPECIES_COUNT: count,
                    self.N50_QUANTILES: n50_quantiles,
                    self.CONTIGS_QUANTILES: contigs_quantiles,
                    self.L50_QUANTILES: l50_quantiles,
                    self.LENGTH_QUANTILES: length_quantiles
                }

                self.database[species] = information

    def contains(self, species):
        """
        Returns whether or not the database contains the species.

        PARAMETERS
            species (str): the species, represented as a string

        RETURNS
            present (bool): whether or not the species is represented in the database
        """

        present = True if species in self.database else False

        return present

    def get_count(self, species):
        """
        Returns the count for the specified species. This is the number of times the
        particular species was observed when building the assembly statistics database.

        RETURNS
            count (int): the observed counts for the species when building the database
                returns None if the species is missing
        """

        if species in self.database:
            count = self.database[species][self.SPECIES_COUNT]

        else:
            count = None

        return count

    def get_n50_quantile(self, species, value):
        """
        Returns the N50 quantile for the specified species and quantile value.

        RETURNS
            quantile (float): the N50 quantile for the specified species and quantile value
                returns None if the species or quantile is missing
        """

        if species in self.database:
            n50_quantiles = self.database[species][self.N50_QUANTILES]
            quantile = float(n50_quantiles[value]) if value in n50_quantiles else None

        else:
            quantile = None

        return quantile

    def get_contigs_quantile(self, species, value):
        """
        Returns the number of contigs quantile for the specified species and quantile value.

        RETURNS
            quantile (float): the number of contigs quantile for the specified species and quantile value
                returns None if the species or quantile is missing
        """

        if species in self.database:
            contigs_quantiles = self.database[species][self.CONTIGS_QUANTILES]
            quantile = float(contigs_quantiles[value]) if value in contigs_quantiles else None

        else:
            quantile = None

        return quantile

    def get_l50_quantile(self, species, value):
        """
        Returns the L50 quantile for the specified species and quantile value.

        RETURNS
            quantile (float): the L50 quantile for the specified species and quantile value
                returns None if the species or quantile is missing
        """

        if species in self.database:
            l50_quantiles = self.database[species][self.L50_QUANTILES]
            quantile = float(l50_quantiles[value]) if value in l50_quantiles else None

        else:
            quantile = None

        return quantile

    def get_length_quantile(self, species, value):
        """
        Returns the assembly length quantile for the specified species and quantile value.

        RETURNS
            quantile (float): the assembly length quantile for the specified species and quantile value
                returns None if the species or quantile is missing
        """

        if species in self.database:
            length_quantiles = self.database[species][self.LENGTH_QUANTILES]
            quantile = float(length_quantiles[value]) if value in length_quantiles else None

        else:
            quantile = None

        return quantile
