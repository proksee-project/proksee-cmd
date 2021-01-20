"""
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
"""

import os
from pathlib import Path

# Importing ReadFilterer class from read_filterer.py
from proksee.read_filterer import ReadFilterer
import pytest

#  Defining global variables for testing
from proksee.reads import Reads

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))
TEST_OUTPUT_DIR = '{}/data/testout'.format(str(START_DIR))
JSON = os.path.join(TEST_OUTPUT_DIR, 'fastp.json')
HTML = os.path.join(TEST_OUTPUT_DIR, 'fastp.html')

# Using paired fastq files from illumina public data
forward1 = os.path.join(TEST_INPUT_DIR, 'NA12878_fwd.fastq')
reverse1 = os.path.join(TEST_INPUT_DIR, 'NA12878_rev.fastq')

# Using pacbio single read
forward2 = os.path.join(TEST_INPUT_DIR, 'ATCC_MSA-1003_16S_5reads.fastq.gz')

# Defining instances of ReadFilterer class
read_filtering1 = ReadFilterer(Reads(forward1, reverse1), TEST_OUTPUT_DIR)
read_filtering2 = ReadFilterer(Reads(forward2, None), TEST_OUTPUT_DIR)

# Defining output filtered reads
forward_filt = os.path.join(TEST_OUTPUT_DIR, 'fwd_filtered.fastq')
reverse_filt = os.path.join(TEST_OUTPUT_DIR, 'rev_filtered.fastq')

# Defining fastp expected commands for successful executions of ReadFilterer class methods
fastp_str1 = 'fastp -i ' + forward1 + ' -I ' + reverse1 + ' -o ' + forward_filt + ' -O ' + \
    reverse_filt + ' -j ' + JSON + ' -h ' + HTML
fastp_str2 = 'fastp -i ' + forward2 + ' -o ' + forward_filt + ' -j ' + JSON + ' -h ' + HTML
fastp_func_good = 'FASTP filtered reads'


class TestReadFilter():

    def test_build_fastp_command_paired(self):
        """
        Tests that the correct FASTP command is built when given both forward and reverse reads.
        """

        method_string_good = read_filtering1._ReadFilterer__build_fastp_command()
        assert fastp_str1 == method_string_good

    def test_build_fastp_command_single(self):
        """
        Tests that the correct FASTP command is built when only given forward reads.
        """

        method_string_good = read_filtering2._ReadFilterer__build_fastp_command()
        assert fastp_str2 == method_string_good

    def test_filter_reads_missing_files(self):
        """
        Tests that a FileNotFoundError is raised when read files are missing.
        """

        # forward missing
        forward = 'does_not_exist.fastq'
        reverse = None
        read_filterer = ReadFilterer(Reads(forward, reverse), TEST_OUTPUT_DIR)

        with pytest.raises(FileNotFoundError):
            assert read_filterer.filter_reads()

        # reverse missing
        forward = os.path.join(TEST_INPUT_DIR, 'NA12878_fwd.fastq')
        reverse = 'does_not_exist.fastq'
        read_filterer = ReadFilterer(Reads(forward, reverse), TEST_OUTPUT_DIR)

        with pytest.raises(FileNotFoundError):
            assert read_filterer.filter_reads()

        # forward good, reverse 'None' -- no error
        forward = os.path.join(TEST_INPUT_DIR, 'NA12878_fwd.fastq')
        reverse = None
        read_filterer = ReadFilterer(Reads(forward, reverse), TEST_OUTPUT_DIR)

        filtered_reads = read_filterer.filter_reads()
        assert os.path.isfile(filtered_reads.forward)
        assert filtered_reads.reverse is None

    def test_filter_reads_simple(self):
        """
        Tests a simple, expected execution of read filtering.
        """

        reads = Reads(forward1, reverse1)
        filterer = ReadFilterer(reads, TEST_OUTPUT_DIR)

        filtered_reads = filterer.filter_reads()

        assert filtered_reads.forward == os.path.join(TEST_OUTPUT_DIR, 'fwd_filtered.fastq')
        assert filtered_reads.reverse == os.path.join(TEST_OUTPUT_DIR, 'rev_filtered.fastq')
        assert os.path.isfile(filtered_reads.forward)
        assert os.path.isfile(filtered_reads.reverse)
