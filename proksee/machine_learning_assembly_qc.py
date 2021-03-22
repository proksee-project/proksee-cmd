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
import math
import warnings

DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database")
DATABASE_FILENAME = "species_median_log_metrics.txt"
MACHINE_LEARNING_MODEL_FILENAME = "random_forest_n50_numcontigs_l50_length_gccontent.joblib"


class NormalizedDatabase():
    """
    A class representing a database of median or median-log values
    of genomic assembly attributes (list of floats) for different species

    ATTRIBUTES
        database (dict): a dictionary mapping species (str) to assembly attributes (list of floats)
    """

    # Constants for assembly attributes to identify array indices
    N50 = 0
    NUM_CONTIGS = 1
    L50 = 2
    LENGTH = 3
    GENOME_COVERAGE = 4
    GC_CONTENT = 5

    def __init__(self):
        """
        Initializes the database
        """

        self.database = {}
        self.create_dictionary_database()

    def create_dictionary_database(self):
        """
        Creates dictionary of database of median normalized genomic attributes (list of floats)

        POST
            The database dictionary will be created as a class attribute called 'database'
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

    def get_median_log_n50(self, species_name):
        """
        Returns median value of log(n50) of a species from the database

        PARAMETERS
            species_name (str): string representation of a species

        RETURNS
            median_log_n50 (float): median of log(n50) of a species in the database
        """

        median_log_n50 = self.database[species_name][self.N50]

        return median_log_n50

    def get_median_log_num_contigs(self, species_name):
        """
        Returns median value of log(number of contigs) of a species from the database

        PARAMETERS
            species_name (str): string representation of a species

        RETURNS
            median_log_num_contigs (float): median of log(number of contigs) of a species in the database
        """

        median_log_num_contigs = self.database[species_name][self.NUM_CONTIGS]

        return median_log_num_contigs

    def get_median_log_l50(self, species_name):
        """
        Returns median value of log(l50) of a species from the database

        PARAMETERS
            species_name (str): string representation of a species

        RETURNS
            median_log_l50 (float): median of log(l50) of a species in the database
        """

        median_log_l50 = self.database[species_name][self.L50]

        return median_log_l50

    def get_median_log_length(self, species_name):
        """
        Returns median value of log(assembly length) of a species from the database

        PARAMETERS
            species_name (str): string representation of a species

        RETURNS
            median_log_length (float): median of log(assembly length) of a species in the database
        """

        median_log_length = self.database[species_name][self.LENGTH]

        return median_log_length

    def get_median_gc_content(self, species_name):
        """
        Returns median value of gc content of a species from the database

        PARAMETERS
            species_name (str): string representation of a species

        RETURNS
            median_gc_content (float) : median of gc content of a species in the database
        """

        median_gc_content = self.database[species_name][self.GC_CONTENT]

        return median_gc_content

    def normalize_assembly_statistics(self, species_name, n50, num_contigs, l50, length, gc_content):
        """
        Normalizes class attributes (n50, num_contigs, l50, length, gc_content)
        and returns numpy vector

        PARAMETERS
            species_name (str): string representation of a species
            n50 (int): shortest contig at 50% of the assembly length
            num_contigs (int): the number of contigs in the assembly
            l50 (int): smallest number of contigs summing up to 50% of the assembly length
            length (int): the total assembly length
            gc_content (float): the GC-ratio of the bases in the assembly

        RETURNS
            normalized_assembly_statistics (numpy array): numpy vector of normalized genomic attributes
        """

        if (n50 <= 0 or num_contigs <= 0 or l50 <= 0 or
                length <= 0 or gc_content < 0):
            raise ValueError('One or more genomic attributes are numerically incompatible. ' +
                             'Machine learning evaluation cannot be done.')

        elif (math.isnan(n50) or math.isnan(num_contigs) or math.isnan(l50) or
                math.isnan(length) or math.isnan(gc_content)):
            raise ValueError('One or more genomic attributes are missing. ' +
                             'Machine learning evaluation cannot be done.')

        else:
            # Log transformation and median normalization of assembly attributes
            input_logn50 = round(np.log10(n50), 3)
            normalized_n50 = input_logn50 - self.get_median_log_n50(species_name)

            input_lognumcontigs = round(np.log10(num_contigs), 3)
            normalized_numcontigs = (input_lognumcontigs -
                                     self.get_median_log_num_contigs(species_name))

            input_logl50 = round(np.log10(l50), 3)
            normalized_l50 = input_logl50 - self.get_median_log_l50(species_name)

            input_loglength = round(np.log10(length), 3)
            normalized_length = input_loglength - self.get_median_log_length(species_name)

            normalized_gccontent = gc_content - self.get_median_gc_content(species_name)

            normalized_assembly_array = [normalized_n50, normalized_numcontigs,
                                         normalized_l50, normalized_length, normalized_gccontent]

            # Numpy vectorization of array
            normalized_assembly_statistics = np.reshape(normalized_assembly_array, (1, -1))

            return normalized_assembly_statistics


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
        normalized_database (NormalizedDatabase): normalized assembly attributes
    """

    def __init__(self, species, n50, num_contigs, l50, length, gc_content, normalized_database):
        """
        Initializes the MachineLearningAssemblyQC object

        PARAMETERS:
            species (Species): the Species object representing the species
            n50 (int): shortest contig at 50% of the assembly length
            num_contigs (int): the number of contigs in the assembly
            l50 (int): smallest number of contigs summing up to 50% of the assembly length
            length (int): the total assembly length
            gc_content (float): the GC-ratio of the bases in the assembly
            normalized_database (NormalizedDatabase): normalized assembly attributes
        """

        self.species = species
        self.n50 = n50
        self.num_contigs = num_contigs
        self.l50 = l50
        self.length = length
        self.gc_content = gc_content
        self.normalized_database = normalized_database

    def calculate_probability(self):
        """
        Loads a pre-trained random forest machine learning model and evaluates assembly metrics

        RETURNS
            predicted_value (float): Prediction probability of the assembly resembling an NCBI reference
            sequence assembly
        """

        normalized_assembly_statistics = self.normalized_database.normalize_assembly_statistics(
            self.species.name, self.n50, self.num_contigs, self.l50, self.length, self.gc_content
        )

        # Ignore numpy.ufunc warning (mostly benign, see: github.com/numpy/numpy/issues/11788)
        warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

        random_forest_model = joblib.load(os.path.join(DATABASE_PATH, MACHINE_LEARNING_MODEL_FILENAME))
        prediction_array = random_forest_model.predict_proba(normalized_assembly_statistics)
        predicted_value = prediction_array[0, 0]

        return float(predicted_value)
