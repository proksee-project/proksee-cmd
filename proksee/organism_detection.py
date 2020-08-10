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


    def refseq_masher_string(self, forward, reverse):
        if reverse is None:
            ref_str = 'refseq_masher matches ' + forward
        elif reverse.endswith('fastq') or reverse.endswith('fq'):
            ref_str = 'refseq_masher matches ' + forward + ' ' + reverse
        
        return ref_str


    def refseq_masher_func(self, ref_str, output_dir):
        refseq_out = os.path.join(output_dir, 'refseq.out')
        refseq_log = os.path.join(output_dir, 'refseq.log')
        stdout = open(refseq_out, 'w+')
        stderr = open(refseq_log, 'w+')
        try:
            subprocess.call(ref_str, shell=True, stdout=stdout, stderr=stderr)
        except subprocess.CalledProcessError as e:
            raise e

        return refseq_out


    def identify_organism(self, refseq_out):
        '''Initiating counting of output organisms'''
        organism_counter = defaultdict(int)

        '''Opening refseq_masher output file'''
        with open(refseq_out, 'r') as open_file:
            for line in open_file:

                '''Leaving out blank lines and isolating 2nd column'''
                if len(line.strip()) > 0:
                    col2 = line.split('\t')[1]

                    try:
                        '''Joining genus and species name, counting occurrences'''
                        test_organism = col2.split(' ')[0] + ' ' + col2.split(' ')[1]
                        organism_counter[test_organism] += 1

                    except Exception:
                        pass

        try:
            '''Output organism with highest number of occurrences'''
            major_org = max(organism_counter.items(), key=operator.itemgetter(1))[0]
        except Exception:
            pass
        
        return major_org


    def major_organism(self, forward, reverse, output_dir):
        refseq_string = self.refseq_masher_string(forward, reverse)
        refseq_out = self.refseq_masher_func(refseq_string, output_dir)
        major_org = self.identify_organism(refseq_out)

        output_string = 'Major reference organism is {}'.format(major_org)

        return output_string
