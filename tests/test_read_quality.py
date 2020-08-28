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

# Importing ReadFiltering class from read_quality.py
from proksee.read_quality import ReadFiltering
import subprocess
import pytest

#  Defining global variables for testing
START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))
TEST_OUTPUT_DIR = '{}/data/testout'.format(str(START_DIR))
JSON = os.path.join(TEST_OUTPUT_DIR, 'fastp.json')
HTML = os.path.join(TEST_OUTPUT_DIR, 'fastp.html')
RETURN_CODE = 0

# Using paired fastq files from illumina public data
forward1 = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_fwd.fastq')
reverse1 = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_rev.fastq')

# Using pacbio single read
forward2 = os.path.join(TEST_INPUT_DIR, 'ATCC_MSA-1003_16S_5reads.fastq.gz')

# Defining instances of ReadFiltering class
read_filtering1 = ReadFiltering(forward1, reverse1, TEST_OUTPUT_DIR)
read_filtering2 = ReadFiltering(forward2, None, TEST_OUTPUT_DIR)

# Defining output filtered reads
forward_filt = os.path.join(TEST_OUTPUT_DIR, 'fwd_filtered.fastq')
reverse_filt = os.path.join(TEST_OUTPUT_DIR, 'rev_filtered.fastq')

# Defining fastp expected commands for successful executions of ReadFiltering class methods
fastp_str1 = 'fastp -i ' + forward1 + ' -I ' + reverse1 + ' -o ' + forward_filt + ' -O ' + \
    reverse_filt + ' -j ' + JSON + ' -h ' + HTML
fastp_str2 = 'fastp -i ' + forward2 + ' -o ' + forward_filt + ' -j ' + JSON + ' -h ' + HTML


class TestReadFilter():

    # Test for checking good fastp string
    def test_fastp_string1_good(self):
        method_string_good = read_filtering1._ReadFiltering__fastp_string()
        assert fastp_str1 == method_string_good

    # Test for negating bad fastp string
    def test_fastp_string1_bad(self):
        fastp_str_bad = 'fastp -i ' + forward1
        method_string_good = read_filtering1._ReadFiltering__fastp_string()
        assert fastp_str_bad != method_string_good

    # Test for fastp function with paired illumina reads
    def test_fastp_func1_good(self):
        method_rc = read_filtering1._ReadFiltering__fastp_func(fastp_str1)
        assert RETURN_CODE == method_rc

    # Test for fastp function with incorrect parameters
    def test_fastp_func1_badparams(self):
        fastp_str_bad = 'fastp --incorrect params'
        with pytest.raises(subprocess.CalledProcessError):
            assert read_filtering1._ReadFiltering__fastp_func(fastp_str_bad)

    # Test for fastp function when fastp isn't installed
    def test_fastp_func1_badcommand(self):
        fastp_str_bad = 'conda deactivate && fastp -h'
        with pytest.raises(subprocess.CalledProcessError):
            assert read_filtering1._ReadFiltering__fastp_func(fastp_str_bad)

    # Test for ReadFiltering class method integrating all methods
    def test_filter_read1_good(self):
        fastp_output_string_good = 'FASTP filtered reads written to output directory. Return code ' + str(RETURN_CODE)
        method_string = read_filtering1.filter_read()
        assert fastp_output_string_good == method_string

    # Test for failed integrating method
    def test_filter_read1_bad(self):
        forward_bad = 'does_not_exist.fastq'
        read_filtering_bad = ReadFiltering(forward_bad, None, TEST_OUTPUT_DIR)
        with pytest.raises(subprocess.CalledProcessError):
            assert read_filtering_bad.filter_read()

    # Test for fastp string with single read
    def test_fastp_string2_good(self):
        method_string_good = read_filtering2._ReadFiltering__fastp_string()
        assert fastp_str2 == method_string_good

    # Test for fastp function with single read
    def test_fastp_func2_good(self):
        method_rc = read_filtering2._ReadFiltering__fastp_func(fastp_str2)
        assert RETURN_CODE == method_rc

    # Test for ReadFiltering integrating method with single read
    def test_filter_read2_good(self):
        fastp_output_string_good = 'FASTP filtered reads written to output directory. Return code ' + str(RETURN_CODE)
        method_string = read_filtering2.filter_read()
        assert fastp_output_string_good == method_string
