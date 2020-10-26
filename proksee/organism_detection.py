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

import os
import subprocess
from collections import defaultdict


from proksee.species import Species


# Defining organism detection class for identifying reference genome organism
class OrganismDetection():

    # Defining __init__ method with reads and output directory parameters
    def __init__(self, forward, reverse, output_dir):
        self.forward = forward
        self.reverse = reverse
        self.output_dir = output_dir

    # Creating refseq_masher command to be executed
    def __refseq_masher_string(self):
        if self.reverse is None:
            ref_str = 'refseq_masher matches ' + self.forward

        else:
            ref_str = 'refseq_masher matches ' + self.forward + ' ' + self.reverse

        return ref_str

    # Method for running refseq_masher command
    def __refseq_masher_func(self, ref_str):
        '''Creating refseq_masher output and log files'''
        refseq_out = os.path.join(self.output_dir, 'refseq.out')
        refseq_log = open(os.path.join(self.output_dir, 'refseq.log'), 'w+')
        stdout = open(refseq_out, 'w+')

        '''Running refseq_masher as a subprocess module. Returning output file.
        Raising error otherwise'''
        try:
            subprocess.check_call(ref_str, shell=True, stdout=stdout, stderr=refseq_log)
            return refseq_out
        except subprocess.CalledProcessError as e:
            raise e

    # Method for identifying major reference genome from refseq_masher output
    def __identify_organism(self, refseq_out):
        '''Initiating counting of output organisms'''
        organism_counter_uniq = defaultdict(int)
        total_organism_count = 0
        probability = {}

        '''Opening refseq_masher output file'''
        with open(refseq_out, 'r') as open_file:
            for line in open_file:

                '''Leaving out blank lines and isolating 2nd column'''
                if len(line.strip()) > 0:

                    '''Splitting 2nd column by spaces to get organism name'''
                    try:
                        list_col2 = line.split('\t')[1].split(' ')

                        '''Joining genus and species name, counting unique and total occurrences'''
                        test_organism = list_col2[0] + ' ' + list_col2[1]
                        organism_counter_uniq[test_organism] += 1
                        total_organism_count += 1

                        '''Raising exception if second column does not contain spaces'''
                    except IndexError:
                        pass

        '''Output organism with highest number of occurrences'''
        if organism_counter_uniq:
            mx = max(organism_counter_uniq.values())
            for key, value in organism_counter_uniq.items():
                if value == mx:

                    '''Calculating probability of organism/s with max occurences'''
                    probability[key] = round(value/total_organism_count, 2)

        else:
            pass

            '''Appending major reference organism/s name/s and probability values to output string'''

        species_list = []

        for key, value in probability.items():
            name = key
            confidence = value
            species_list.append(Species(name, confidence))

        species_list.sort(key=lambda x: x.confidence, reverse=True)

        return species_list

    # Method for integrating private functions
    def major_organism(self):
        refseq_string = self.__refseq_masher_string()
        refseq_out = self.__refseq_masher_func(refseq_string)
        species_list = self.__identify_organism(refseq_out)

        return species_list
