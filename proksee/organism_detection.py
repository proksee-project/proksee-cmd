import os
import sys
import subprocess, shlex
import pandas as pd
from collections import defaultdict
import operator

class OrganismDetection():


    def __init__(self, forward, reverse, output_dir):
        self.forward = forward
        self.reverse = reverse
        self.output_dir = output_dir


    def __refseq_masher_string(self):
        if self.reverse is None:
            ref_str = 'refseq_masher matches ' + self.forward
        else:
            ref_str = 'refseq_masher matches ' + self.forward + ' ' + self.reverse
        
        return ref_str


    def __refseq_masher_func(self, ref_str):
        refseq_out = os.path.join(self.output_dir, 'refseq.out')
        refseq_log = os.path.join(self.output_dir, 'refseq.log')
        stdout = open(refseq_out, 'w+')
        stderr = open(refseq_log, 'w+')
        try:
            rc = subprocess.call(ref_str, shell=True, stdout=stdout, stderr=stderr)
        except subprocess.CalledProcessError as e:
            raise e

        return refseq_out, rc


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
                    col2 = line.split('\t')[1]

                    try:
                        '''Joining genus and species name, counting occurrences'''
                        test_organism = col2.split(' ')[0] + ' ' + col2.split(' ')[1]
                        organism_counter_uniq[test_organism] += 1
                        total_organism_count += 1
                    except Exception:
                        pass

        try:
            '''Output organism with highest number of occurrences'''
            mx = max(organism_counter_uniq.values())
            for key, value in organism_counter_uniq.items():
                if value == mx:
                    probability[key] = round(value/total_organism_count , 2)
        except Exception:
            pass

        org_string = ''
        for key, value in probability.items():
            org_string += key + ' (probability : ' + str(value) + '), '
        
        return org_string


    def major_organism(self):
        refseq_string = self.__refseq_masher_string()
        refseq_out, return_code = self.__refseq_masher_func(refseq_string)
        major_org = self.__identify_organism(refseq_out)

        output_string = 'Major reference organism is/are {}. Return code {}'.format(major_org, return_code)

        return output_string
