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
    N50_05 = 1  # the 0.05 quantile of the N50
    N50_20 = 2  # the 0.20 quantile of the N50
    N50_80 = 3
    N50_95 = 4
    CONTIG_05 = 5   # the 0.05 quantile of the number of contigs
    CONTIG_20 = 6   # the 0.20 quantile of the number of contigs
    CONTIG_80 = 7
    CONTIG_95 = 8
    L50_05 = 9   # the 0.05 quantile of the L50
    L50_20 = 10  # the 0.20 quantile of the L50
    L50_80 = 11
    L50_95 = 12
    LENGTH_05 = 13  # the 0.05 quantile of the assembly length
    LENGTH_20 = 14  # the 0.20 quantile of the assembly length
    LENGTH_80 = 15
    LENGTH_95 = 16

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

                information = {
                    self.N50_05: row[self.N50_05],
                    self.N50_20: row[self.N50_20],
                    self.N50_80: row[self.N50_80],
                    self.N50_95: row[self.N50_95],
                    self.CONTIG_05: row[self.CONTIG_05],
                    self.CONTIG_20: row[self.CONTIG_20],
                    self.CONTIG_80: row[self.CONTIG_80],
                    self.CONTIG_95: row[self.CONTIG_95],
                    self.L50_05: row[self.L50_05],
                    self.L50_20: row[self.L50_20],
                    self.L50_80: row[self.L50_80],
                    self.L50_95: row[self.L50_95],
                    self.LENGTH_05: row[self.LENGTH_05],
                    self.LENGTH_20: row[self.LENGTH_20],
                    self.LENGTH_80: row[self.LENGTH_80],
                    self.LENGTH_95: row[self.LENGTH_95]
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

    def get_n50_05(self, species):
        """
        Returns the 0.05 quantile for the N50.

        RETURNS
            n50_05 (int): the 0.05 quantile for the N50
        """

        return int(self.database[species][self.N50_05]) if species in self.database else None

    def get_n50_20(self, species):
        """
        Returns the 0.20 quantile for the N50.

        RETURNS
            n50_20 (int): the 0.20 quantile for the N50
        """

        return int(self.database[species][self.N50_20]) if species in self.database else None

    def get_n50_80(self, species):
        """
        Returns the 0.80 quantile for the N50.

        RETURNS
            n50_80 (int): the 0.80 quantile for the N50
        """

        return int(self.database[species][self.N50_80]) if species in self.database else None

    def get_n50_95(self, species):
        """
        Returns the 0.95 quantile for the N50.

        RETURNS
            n50_95 (int): the 0.95 quantile for the N50
        """

        return int(self.database[species][self.N50_95]) if species in self.database else None

    def get_contig_05(self, species):
        """
        Returns the 0.05 quantile for the number of contigs.

        RETURNS
            contig_05 (int): the 0.05 quantile for the number of contigs
        """

        return int(self.database[species][self.CONTIG_05]) if species in self.database else None

    def get_contig_20(self, species):
        """
        Returns the 0.20 quantile for the number of contigs.

        RETURNS
            contig_20 (int): the 0.20 quantile for the number of contigs
        """

        return int(self.database[species][self.CONTIG_20]) if species in self.database else None

    def get_contig_80(self, species):
        """
        Returns the 0.80 quantile for the number of contigs.

        RETURNS
            contig_80 (int): the 0.80 quantile for the number of contigs
        """

        return int(self.database[species][self.CONTIG_80]) if species in self.database else None

    def get_contig_95(self, species):
        """
        Returns the 0.95 quantile for the number of contigs.

        RETURNS
            contig_95 (int): the 0.95 quantile for the number of contigs
        """

        return int(self.database[species][self.CONTIG_95]) if species in self.database else None

    def get_l50_05(self, species):
        """
        Returns the 0.05 quantile for the L50.

        RETURNS
            L50_05 (int): the 0.05 quantile for the L50
        """

        return int(self.database[species][self.L50_05]) if species in self.database else None

    def get_l50_20(self, species):
        """
        Returns the 0.20 quantile for the L50.

        RETURNS
            L50_20 (int): the 0.20 quantile for the L50
        """

        return int(self.database[species][self.L50_20]) if species in self.database else None

    def get_l50_80(self, species):
        """
        Returns the 0.80 quantile for the L50.

        RETURNS
            L50_80 (int): the 0.80 quantile for the L50
        """

        return int(self.database[species][self.L50_80]) if species in self.database else None

    def get_l50_95(self, species):
        """
        Returns the 0.95 quantile for the L50.

        RETURNS
            L50_95 (int): the 0.95 quantile for the L50
        """

        return int(self.database[species][self.L50_95]) if species in self.database else None

    def get_length_05(self, species):
        """
        Returns the 0.05 quantile for the assembly length.

        RETURNS
            length_05 (int): the 0.05 quantile for the assembly length
        """

        return int(self.database[species][self.LENGTH_05]) if species in self.database else None

    def get_length_20(self, species):
        """
        Returns the 0.20 quantile for the assembly length.

        RETURNS
            length_20 (int): the 0.20 quantile for the assembly length
        """

        return int(self.database[species][self.LENGTH_20]) if species in self.database else None

    def get_length_80(self, species):
        """
        Returns the 0.80 quantile for the assembly length.

        RETURNS
            length_80 (int): the 0.80 quantile for the assembly length
        """

        return int(self.database[species][self.LENGTH_80]) if species in self.database else None

    def get_length_95(self, species):
        """
        Returns the 0.95 quantile for the assembly length.

        RETURNS
            length_95 (int): the 0.95 quantile for the assembly length
        """

        return int(self.database[species][self.LENGTH_95]) if species in self.database else None
