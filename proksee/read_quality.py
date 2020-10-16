'''
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
'''

import os
import subprocess


# Defining read filtering class for filtering reads using fastp
class ReadFiltering():

    # Defining __init__ method with reads and output directory parameters
    def __init__(self, forward, reverse, output_dir):
        self.forward = forward
        self.reverse = reverse
        self.output_dir = output_dir

    # Creating fastp command to be executed
    def __fastp_string(self):
        '''specifying fixed output files for fastp'''
        out1 = os.path.join(self.output_dir, 'fwd_filtered.fastq')
        out2 = os.path.join(self.output_dir, 'rev_filtered.fastq')
        json = os.path.join(self.output_dir, 'fastp.json')
        html = os.path.join(self.output_dir, 'fastp.html')

        '''Creating fastp command based on absence/presence of reverse read'''
        if self.reverse is None:
            fastp_str = 'fastp -i ' + self.forward + ' -o ' + \
                out1 + ' -j ' + json + ' -h ' + html
        else:
            fastp_str = 'fastp -i ' + self.forward + ' -I ' + self.reverse + \
                ' -o ' + out1 + ' -O ' + out2 + ' -j ' + json + ' -h ' + html

        return fastp_str

    # Method for running fastp command
    def __fastp_func(self, fastp_str):
        '''Creating fastp log file'''
        fastp_log = open(os.path.join(self.output_dir, 'fastp.log'), 'w+')

        '''Running fastp as a subprocess module. Raising error otherwise'''
        try:
            subprocess.check_call(fastp_str, shell=True, stderr=fastp_log)
            success = 'FASTP filtered reads'
        except subprocess.CalledProcessError as e:
            raise e

        return success

    # Method for integrating private functions
    def filter_read(self):
        fastp_string = self.__fastp_string()
        fastp_func = self.__fastp_func(fastp_string)
        output_string = fastp_func + ' written to output directory'

        return output_string


class ReadQuality:

    def __init__(self, total_reads, total_bases, q20_bases, q30_bases, forward_median_length, reverse_median_length,
                 gc_content):

        self.total_reads = total_reads
        self.total_bases = total_bases
        self.q20_bases = q20_bases
        self.q30_bases = q30_bases

        self.q20_rate = q20_bases / total_bases
        self.q30_rate = q30_bases / total_bases

        self.forward_median_length = forward_median_length
        self.reverse_median_length = reverse_median_length

        self.gc_content = gc_content
