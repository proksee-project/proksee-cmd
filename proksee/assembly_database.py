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

import csv


class AssemblyDatabase:
    """
    A class representing a database containing aggregate information about assemblies for different species.

    ATTRIBUTES
        database (dict): a dictionary mapping species to assembly information
        database_filename (str): the filename of the database
    """

    SPECIES = 0
    CONTIGS_MEAN = 1
    CONTIGS_STD = 2
    ASSEMBLY_SIZE_MEAN = 3
    ASSEMBLY_SIZE_STD = 4
    N50_MEAN = 5
    N50_STD = 6

    def __init__(self, database_filename):
        """
        Initializes the database.

        PARAMETERS
            database_filename (str): the filename of the assembly database
        """

        self.database = {}
        self.database_filename = database_filename

        self.load()

    def load(self):
        """
        Loads the database.
        """

        self.database = {}

        with open(self.database_filename) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            next(reader)  # skip headers

            for row in reader:
                species = row[self.SPECIES]

                information = {
                    self.CONTIGS_MEAN: row[self.CONTIGS_MEAN],
                    self.CONTIGS_STD: row[self.CONTIGS_STD],
                    self.ASSEMBLY_SIZE_MEAN: row[self.ASSEMBLY_SIZE_MEAN],
                    self.ASSEMBLY_SIZE_STD: row[self.ASSEMBLY_SIZE_STD],
                    self.N50_MEAN: row[self.N50_MEAN],
                    self.N50_STD: row[self.N50_STD]
                }

                self.database[species] = information

        print(self.database)

    def get_contigs_mean(self, species):
        """
        Returns the mean contigs for a given species.

        RETURNS
            contigs_mean (int): The mean number of contigs or None if the species does not exist in the database.
        """

        return self.database[species][self.CONTIGS_MEAN] if species in self.database else None

    def get_contigs_std(self, species):
        """
        Returns the standard deviation of contigs for a given species.

        RETURNS
            contigs_std (float): The standard deviation of contigs or None if the species does not exist in the
                database.
        """

        return self.database[species][self.CONTIGS_STD] if species in self.database else None

    def get_assembly_size_mean(self, species):
        """
        Returns the mean assembly size for a given species.

        RETURNS
            assembly_size_mean (int): The mean assembly size or None if the species does not exist in the database.
        """

        return self.database[species][self.ASSEMBLY_SIZE_MEAN] if species in self.database else None

    def get_assembly_size_std(self, species):
        """
        Returns the standard deviation of the assembly size for a given species.

        RETURNS
            assembly_size_std (float): The standard deviation of assembly size or None if the species does not exist
                in the database.
        """

        return self.database[species][self.ASSEMBLY_SIZE_STD] if species in self.database else None

    def get_n50_mean(self, species):
        """
        Returns the mean n50 for a given species.

        RETURNS
            n50_mean (int): The mean n50 or None if the species does not exist in the database.
        """

        return self.database[species][self.N50_MEAN] if species in self.database else None

    def get_n50_std(self, species):
        """
        Returns the standard deviation of the n50 for a given species.

        RETURNS
            n50_std (float): The standard deviation of the n50 or None if the species does not exist in the database.
        """

        return self.database[species][self.N50_STD] if species in self.database else None
