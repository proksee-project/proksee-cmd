'''
Copyright:

University of Manitoba & National Microbiology Laboratory, Canada, 2020

Written by: Arnab Saha Mandal

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
'''

import os
import numpy as np
import joblib
from pathlib import Path

DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database")
DATABASE_FILENAME = "species_median_log_metrics.txt"
MACHINE_LEARNING_MODEL_FILENAME = "random_forest_n50_numcontigs_l50_length_gccontent.joblib"


class NormalizedDatabase():
    """
    A class representing database of median or median-log values
    of genomic assembly attributes for different species

    ATTRIBUTES
        database (dict): a dictionary mapping species to assembly atttributes
        create_dictionary_database (function): function to create database object
    """

    def __init__(self):
        """
        Initializes the database

        PARAMETERS
            database (dict): a dictionary mapping species to assembly atttributes
            create_dictionary_database (function): function to create database object
        """

        self.database = {}
        self.create_dictionary_database()

    def create_dictionary_database(self):
        """
        Creates dictionary of database of median normalized genomic attributes

        POST
            The dictionary is created upon initialization of the class
        """

        database_file = open(os.path.join(DATABASE_PATH, DATABASE_FILENAME), 'r')

        # Skips header
        next(database_file)

        for line in database_file:
            row = line.rstrip().split('\t')
            species_name = row[0]

            # Species specific median log(n50), log(num_contigs), log(l50), log(length), log(coverage)
            # and gc_content written in order as a list.
            species_info = [float(i) for i in row[1:]]
            self.database[species_name] = species_info

    def contains(self, species_name):
        """
        Checks if species is present in the database

        PARAMETERS
            species_name (str): string representation of a species

        RETURNS
            species_present (bool): presence/absence of species in the database
        """

        species_present = True if species_name in self.database else False

        return species_present


class MachineLearningAssemblyQC():
    """
    A class representing machine learning based evaluation of genomic assembly attributes

    ATTRIBUTES:
        database (database): database object
        species (Species): the Species object representing the species
        n50 (int): shortest contig at 50% of the assembly length
        num_contigs (int): the number of contigs in the assembly
        l50 (int): smallest number of contigs summing up to 50% of the assembly length
        length (int): the total assembly length
        gc_content (float): the GC-ratio of the bases in the assembly
    """

    def __init__(self, database, species, n50, num_contigs, l50, length, gc_content):
        """
        Initializes the MachineLearningAssemblyQC object

        PARAMETERS:
            database (database): database object
            species (Species): the Species object representing the species
            n50 (int): shortest contig at 50% of the assembly length
            num_contigs (int): the number of contigs in the assembly
            l50 (int): smallest number of contigs summing up to 50% of the assembly length
            length (int): the total assembly length
            gc_content (float): the GC-ratio of the bases in the assembly
        """

        self.database = database
        self.species = species
        self.n50 = n50
        self.num_contigs = num_contigs
        self.l50 = l50
        self.length = length
        self.gc_content = gc_content

    def __normalize_vectorize_assembly(self):
        """
        Normalizes input assembly metrics and outputs them to a numpy 1D array

        RETURNS
            normalized_assembly_numpy_row (numpy array): numpy vector of normalized genomic attributes
        """

        # Constants for assembly attributes to identify array indices
        N50 = 0
        NUM_CONTIGS = 1
        L50 = 2
        LENGTH = 3
        GC_CONTENT = 5

        # Dictionary representation of database
        database_dict = self.database.__dict__['database']

        # Log transformation and median normalization of assembly attributes
        input_logn50 = round(np.log10(self.n50), 3)
        normalized_n50 = input_logn50 - database_dict[self.species.name][N50]

        input_lognumcontigs = round(np.log10(self.num_contigs), 3)
        normalized_numcontigs = input_lognumcontigs - database_dict[self.species.name][NUM_CONTIGS]

        input_logl50 = round(np.log10(self.l50), 3)
        normalized_l50 = input_logl50 - database_dict[self.species.name][L50]

        input_loglength = round(np.log10(self.length), 3)
        normalized_length = input_loglength - database_dict[self.species.name][LENGTH]

        normalized_gccontent = self.gc_content - database_dict[self.species.name][GC_CONTENT]

        normalized_assembly_array = [normalized_n50, normalized_numcontigs,
                                     normalized_l50, normalized_length, normalized_gccontent]

        # Numpy vectorization of array
        normalized_assembly_numpy_row = np.reshape(normalized_assembly_array, (1, -1))

        return normalized_assembly_numpy_row

    def __predict_probability(self, normalized_assembly_numpy_row):
        """
        Loads a pre-trained random forest machine learning model and evaluates assembly metrics

        PARAMETERS
            assembly_normalized_numpy_row (numpy array): numpy vector of normalized genomic attributes

        RETURNS
            predicted_value (float): Prediction probability of the assembly being good
        """

        random_forest_model = joblib.load(os.path.join(DATABASE_PATH, MACHINE_LEARNING_MODEL_FILENAME))

        try:
            prediction_array = random_forest_model.predict_proba(normalized_assembly_numpy_row)
            predicted_value = prediction_array[0, 0]

        except ValueError:
            raise ValueError('Missing or numerically incompatible genomic attributes. ' +
                             'Machine learning evaluation cannot be done.')

        return float(predicted_value)

    def machine_learning_probability(self):
        """
        Reads median database, parses input assembly attributes and returns machine learning prediction

        RETURNS
            probability (float): Prediction probability of the assembly being good
        """

        assembly_normalized_numpy_row = self.__normalize_vectorize_assembly()
        probability = self.__predict_probability(assembly_normalized_numpy_row)

        return probability
