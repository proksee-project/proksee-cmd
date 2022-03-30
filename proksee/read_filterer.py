"""
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
"""

import os
import subprocess

from proksee.parser.read_quality_parser import parse_read_quality_from_fastp
from proksee.reads import Reads


class ReadFilterer():
    """
    A class for filtering reads.

    ATTRIBUTES
        reads (Reads): the reads to filter
        output_directory (str): the file location of the output directory for writing files
    """

    LOGFILE_FILENAME = "fastp.log"
    FWD_FILTERED_FILENAME = "fwd_filtered.fastq"
    REV_FILTERED_FILENAME = "rev_filtered.fastq"

    def __init__(self, reads, output_directory):
        """
        Initializes the read filterer.

        PARAMETERS
            reads (Reads): the reads to filter
            output_directory (str): the file location of the output directory for writing files
        """

        self.reads = reads
        self.output_directory = output_directory

    def __build_fastp_command(self):
        """
        Builds the command for running the FASTP program.

        RETURNS
            command (str): a string for running the FASTP program
        """

        forward_reads = self.reads.forward
        reverse_reads = self.reads.reverse

        self.forward_filtered = os.path.join(self.output_directory, self.FWD_FILTERED_FILENAME)
        self.reverse_filtered = os.path.join(self.output_directory,
                                             self.REV_FILTERED_FILENAME) if reverse_reads else None
        json = os.path.join(self.output_directory, 'fastp.json')
        html = os.path.join(self.output_directory, 'fastp.html')

        '''Creating fastp command based on absence/presence of reverse read'''
        if reverse_reads is None:
            command = 'fastp -i ' + forward_reads + ' -o ' + \
                self.forward_filtered + ' -j ' + json + ' -h ' + html
        else:
            command = 'fastp -i ' + forward_reads + ' -I ' + reverse_reads + \
                ' -o ' + self.forward_filtered + ' -O ' + self.reverse_filtered + ' -j ' + json + ' -h ' + html

        return command

    def __run_fastp(self):
        """
        Runs the FASTP program in order to perform filtering on reads.
        """

        logfile_location = open(os.path.join(self.output_directory, self.LOGFILE_FILENAME), 'w+')
        command = self.__build_fastp_command()

        try:
            subprocess.check_call(command, shell=True, stderr=logfile_location)

        except subprocess.CalledProcessError as e:
            raise e

        filtered_reads = Reads(self.forward_filtered, self.reverse_filtered)
        return filtered_reads

    def filter_reads(self):
        """
        Filters reads in order to improve their quality.

        RETURNS
            filtered_reads (Reads): the filtered reads

        POST
            The FASTP program will be run and related files will be written into the output directory.
        """

        if not os.path.isfile(self.reads.forward):
            raise FileNotFoundError("Read input file not found: " + str(self.reads.forward))

        if self.reads.reverse is not None and not os.path.isfile(self.reads.reverse):
            raise FileNotFoundError("Read input file not found: " + str(self.reads.reverse))

        filtered_reads = self.__run_fastp()
        return filtered_reads

    def summarize_quality(self):
        """
        Summarizes the quality of the filtered reads. This function should be run after filtering reads.

        RETURNS
            read_quality (ReadQuality): quality statistics of filtered reads
        """

        json_file = os.path.join(self.output_directory, "fastp.json")

        if os.path.isfile(json_file):
            read_quality = parse_read_quality_from_fastp(json_file)

        return read_quality
