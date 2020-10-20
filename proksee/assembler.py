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


class Assembler:
    """
    A class representing a sequence assembler.

    ATTRIBUTES:
        forward (str): the filename of the forward reads
        reverse (str): the filename of the reverse reads
        output_dir (str): the filename of the output directory
        contigs_filename (str): the filename of the assembled contigs
        log_filename (str): the filename of the logfile
    """

    # Defining __init__ method with reads and output directory parameters
    def __init__(self, forward, reverse, output_dir):
        self.forward = forward
        self.reverse = reverse
        self.output_dir = output_dir

    # Creating skesa command to be executed
    def __skesa_string(self):
        if self.reverse is None:

            '''The flag --use_paired_ends is rightfully used for interleaved reads
            For non-interleaved reads, the flag (or not) doesn't affect output'''
            skesa_str = 'skesa --fastq ' + self.forward + ' --use_paired_ends'

        else:
            skesa_str = 'skesa --fastq ' + self.forward + ',' + self.reverse

        return skesa_str

    # Method for running skesa command
    def __skesa_func(self, skesa_str):
        # Creating skesa output and log files
        self.contigs_filename = os.path.join(self.output_dir, 'skesa.out')
        skesa_out = open(self.contigs_filename, 'w+')

        self.log_filename = os.path.join(self.output_dir, 'skesa.log')
        skesa_log = open(self.log_filename, 'w+')

        '''Running skesa as a subprocess module. Raising error otherwise'''
        try:
            subprocess.check_call(skesa_str, shell=True, stdout=skesa_out, stderr=skesa_log)
            success = 'SKESA assembled reads and log files'
        except subprocess.CalledProcessError as e:
            raise e

        return success

    # Method for integrating private functions
    def perform_assembly(self):
        skesa_string = self.__skesa_string()
        skesa_func = self.__skesa_func(skesa_string)
        output_string = skesa_func + ' written to output directory'

        return output_string
