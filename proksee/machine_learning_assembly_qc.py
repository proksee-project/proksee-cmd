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
from collections import defaultdict
import numpy as np
import joblib
from pathlib import Path

DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database")


class MachineLearningAssemblyQC():
    """
    A class representing machine learning based evaluation of genomic assembly attributes

    ATTRIBUTES:
        species (Species): the Species object representing the species
        n50 (int): shortest contig at 50% of the assembly length
        num_contigs (int): the number of contigs in the assembly
        l50 (int): smallest number of contigs summing up to 50% of the assembly length
        length (int): the total assembly length
        gc_content (float): the GC-ratio of the bases in the assembly
    """

    def __init__(self, species, n50, num_contigs, l50, length, gc_content):
        """
        Initializes the MachineLearningAssemblyQC object

        PARAMETERS:
            species (Species): the Species object representing the species
            n50 (int): shortest contig at 50% of the assembly length
            num_contigs (int): the number of contigs in the assembly
            l50 (int): smallest number of contigs summing up to 50% of the assembly length
            length (int): the total assembly length
            gc_content (float): the GC-ratio of the bases in the assembly
        """

        self.species = species
        self.n50 = n50
        self.num_contigs = num_contigs
        self.l50 = l50
        self.length = length
        self.gc_content = gc_content

    def __read_median_database(self):
        """
        Reads median (or median of logarithm) of genomic attributes from database

        RETURNS
            database (dict): dictionary of median normalized genomic attributes
        """

        database_file = open(os.path.join(DATABASE_PATH, "species_median_log_metrics.txt"), 'r')

        # Skips header
        next(database_file)

        # Initializing dictionary for species
        database = defaultdict(list)
        for line in database_file:
            row = line.rstrip().split('\t')
            species_name = row[0]

            # Species specific median log(n50), log(num_contigs), log(l50), log(length), log(coverage)
            # and gc_content written in order as a list.
            species_info = [float(i) for i in row[1:]]
            database[species_name] = species_info

        return database

    def __normalize_vectorize_assembly(self, database):
        """
        Normalizes input assembly metrics and outputs them to a numpy 1D array

        PARAMETERS
            database (dict): dictionary of median normalized genomic attributes

        RETURNS
            normalized_assembly_numpy_row (numpy array): numpy vector of normalized genomic attributes
        """

        # Constants for assembly attributes to identify array indices
        N50 = 0
        NUM_CONTIGS = 1
        L50 = 2
        LENGTH = 3
        GC_CONTENT = 5

        # Log transformation and median normalization of assembly attributes
        if self.species.name in database:
            input_logn50 = round(np.log10(self.n50), 3)
            normalized_n50 = input_logn50 - database[self.species.name][N50]

            input_lognumcontigs = round(np.log10(self.num_contigs), 3)
            normalized_numcontigs = input_lognumcontigs - database[self.species.name][NUM_CONTIGS]

            input_logl50 = round(np.log10(self.l50), 3)
            normalized_l50 = input_logl50 - database[self.species.name][L50]

            input_loglength = round(np.log10(self.length), 3)
            normalized_length = input_loglength - database[self.species.name][LENGTH]

            normalized_gccontent = self.gc_content - database[self.species.name][GC_CONTENT]

            normalized_assembly_array = [normalized_n50, normalized_numcontigs,
                                         normalized_l50, normalized_length, normalized_gccontent]

            # Numpy vectorization of array
            normalized_assembly_numpy_row = np.reshape(normalized_assembly_array, (1, -1))

        else:
            raise UnboundLocalError('Species missing in database. Machine learning evaluation cannot be done')

        return normalized_assembly_numpy_row

    def __predict_probability(self, normalized_assembly_numpy_row):
        """
        Loads a pre-trained random forest machine learning model and evaluates assembly metrics

        PARAMETERS
            assembly_normalized_numpy_row (numpy array): numpy vector of normalized genomic attributes

        RETURNS
            predicted_value (float): Prediction probability of the assembly being good
        """

        random_forest_model = joblib.load(os.path.join(
            DATABASE_PATH, 'random_forest_n50_numcontigs_l50_length_gccontent.joblib')
        )

        try:
            prediction_arr = random_forest_model.predict_proba(normalized_assembly_numpy_row)
            predicted_value = prediction_arr[0, 0]

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

        database = self.__read_median_database()
        assembly_normalized_numpy_row = self.__normalize_vectorize_assembly(database)
        probability = self.__predict_probability(assembly_normalized_numpy_row)

        return probability
