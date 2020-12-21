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
from pathlib import Path

# Importing ReadFilterer class from read_filterer.py
from proksee.read_filterer import ReadFilterer
import subprocess
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

    # Test for checking good fastp string
    def test_fastp_string1_good(self):
        method_string_good = read_filtering1._ReadFilterer__build_fastp_command()
        assert fastp_str1 == method_string_good

    # Test for negating bad fastp string
    def test_fastp_string1_bad(self):
        fastp_str_bad = 'fastp -i ' + forward1
        method_string_good = read_filtering1._ReadFilterer__build_fastp_command()
        assert fastp_str_bad != method_string_good

    # Test for failed integrating method
    def test_filter_read1_bad(self):
        forward_bad = 'does_not_exist.fastq'
        read_filtering_bad = ReadFilterer(Reads(forward_bad, None), TEST_OUTPUT_DIR)
        with pytest.raises(subprocess.CalledProcessError):
            assert read_filtering_bad.filter_reads()

    # Test for fastp string with single read
    def test_fastp_string2_good(self):
        method_string_good = read_filtering2._ReadFilterer__build_fastp_command()
        assert fastp_str2 == method_string_good
