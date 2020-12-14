'''
Copyright Government of Canada 2020

Written by:

Arnab Saha Mandal
    University of Manitoba
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
from proksee.parser.read_quality_parser import parse_read_quality_from_fastp


class ReadFilterer():
    """
    A class for filtering reads.

    ATTRIBUTES
        forward (str): the file location of the forward reads
        reverse (str): the file location of the reverse reads; may be NULL
        output_dir (str): the file location of the output directory for writing files
        forward_filtered (str): the file location of the filtered forward reads
        reverse_filtered (str): the file location of the filtered reverse reads
    """

    # Defining __init__ method with reads and output directory parameters
    def __init__(self, forward, reverse, output_dir):
        self.forward = forward
        self.reverse = reverse
        self.output_dir = output_dir

    # Creating fastp command to be executed
    def __fastp_string(self):
        '''specifying fixed output files for fastp'''
        self.forward_filtered = os.path.join(self.output_dir, 'fwd_filtered.fastq')
        self.reverse_filtered = os.path.join(self.output_dir, 'rev_filtered.fastq') if self.reverse else None
        json = os.path.join(self.output_dir, 'fastp.json')
        html = os.path.join(self.output_dir, 'fastp.html')

        '''Creating fastp command based on absence/presence of reverse read'''
        if self.reverse is None:
            fastp_str = 'fastp -i ' + self.forward + ' -o ' + \
                self.forward_filtered + ' -j ' + json + ' -h ' + html
        else:
            fastp_str = 'fastp -i ' + self.forward + ' -I ' + self.reverse + \
                ' -o ' + self.forward_filtered + ' -O ' + self.reverse_filtered + ' -j ' + json + ' -h ' + html

        return fastp_str

    # Method for running fastp command
    def __fastp_func(self, fastp_str):
        '''Creating fastp log file'''
        fastp_log = open(os.path.join(self.output_dir, 'fastp.log'), 'w+')

        '''Running fastp as a subprocess module. Raising error otherwise'''
        try:
            subprocess.check_call(fastp_str, shell=True, stderr=fastp_log)

        except subprocess.CalledProcessError as e:
            raise e

    # Method for integrating private functions
    def filter_read(self):
        fastp_string = self.__fastp_string()
        self.__fastp_func(fastp_string)

    def summarize_quality(self):
        json_file = os.path.join(self.output_dir, "fastp.json")
        read_quality = parse_read_quality_from_fastp(json_file)

        return read_quality
