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

class MachineLearningAssemQC():

	def __init__(self, species, n50, contig_count, l50, totlen, gc_content):

		self.species = species
		self.n50 = n50
		self.contig_count = contig_count
		self.l50 = l50
		self.totlen = totlen
		self.gc_content = gc_content

	#load species median log metrics as dictionary with key as species and list of numerical attributes as value
	def __median_log_database_read(self):
		reader_fh = open(os.path.join(DATABASE_PATH, "species_median_log_metrics.txt"), 'r')
		
		#skips header
		next(reader_fh)
		
		#initializing dictionary for species
		sp_log_median_dicn = defaultdict(list)
		for line in reader_fh:
			row = line.rstrip().split('\t')
			sp_info = []
			
			'''
			species specific median logn50, logcontigcount, logl50, logtotlen, logcoverage 
			written in order as a list. The list serves as value to species key
			'''
			for element in range(1, len(row)):
				sp_info.append(float(row[element]))

			sp_log_median_dicn[row[0]] = sp_info

		return sp_log_median_dicn

	'''
	Takes assembly metrics from Quast and species from Mash/Refseq Masher
	Does log transformation and median log normalization of species specific assembly attributes
	Generates numpy vector (single case) to be used as input feed to machine learning model
	'''
	def __assembly_normalize_feedtoml(self, sp_log_median_dicn):

		#log transformation and median normalization of assembly attributes
		try:
			input_logn50 = round(np.log10(self.n50),3)
			normalized_n50 = input_logn50 - sp_log_median_dicn[self.species][0]

			input_logcontigcount = round(np.log10(self.contig_count),3)
			normalized_contigcount = input_logcontigcount - sp_log_median_dicn[self.species][1]

			input_logl50 = round(np.log10(self.l50),3)
			normalized_l50 = input_logl50 - sp_log_median_dicn[self.species][2]

			input_logtotlen = round(np.log10(self.totlen),3)
			normalized_totlen = input_logtotlen - sp_log_median_dicn[self.species][3]

			normalized_gccontent = self.gc_content - sp_log_median_dicn[self.species][5]

			X_test = [normalized_n50, normalized_contigcount, normalized_l50, normalized_totlen, normalized_gccontent]
			X_test_input = np.reshape(X_test, (1, -1))

		except IndexError:
			#Species dictionary for its median metrics does not exist
			raise IndexError('Assembly statistics cannot be normalized and probabilistically evaluated')

		return X_test_input

	#Pass the assembly numpy vector to machine learning model and generate prediction probability
	def __predict_proba(self, X_test):

		loaded_model = joblib.load(os.path.join(DATABASE_PATH,'random_forest_n50_contigcount_l50_totlen_gccontent.joblib'))
		pred_nparr = loaded_model.predict_proba(X_test)
		pred_val = pred_nparr[0,0]
		
		return float(pred_val)

	def machine_learning_proba(self):
		sp_log_median_dicn = self.__median_log_database_read()
		input_vector = self.__assembly_normalize_feedtoml(sp_log_median_dicn)
		probability_ml = self.__predict_proba(input_vector)
		
		return probability_ml
