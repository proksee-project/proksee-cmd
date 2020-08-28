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

# Importing Assembler class from assembler.py
from proksee.assembler import Assembler
import pytest
import subprocess

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))
TEST_OUTPUT_DIR = '{}/data/testout'.format(str(START_DIR))

# Using real fastq files from illumina public data
forward_good = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_fwd.fastq')
reverse_good = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_rev.fastq')

# Using a small truncated read data for catching exceptions
forward_bad = os.path.join(TEST_INPUT_DIR, 'SRR7947278_5pair_reads.fastq')

# Declaring instances of Assembler class
assembler_good = Assembler(forward_good, reverse_good, TEST_OUTPUT_DIR)
assembler_bad = Assembler(forward_bad, None, TEST_OUTPUT_DIR)

# Defining variables for successful executions of Assembler class methods
skesa_str_good = 'skesa --fastq ' + forward_good + ',' + reverse_good
skesa_func_good_rc = 0


class TestAssembler():

    # Test for checking good skesa string
    def test_skesa_string_good(self):
        method_string_good = assembler_good._Assembler__skesa_string()
        assert skesa_str_good == method_string_good

    # Test for negating bad skesa string
    def test_skesa_string_bad(self):
        skesa_str_bad = 'skesa --fastq ' + forward_bad + '--use_paired_ends(deleted whitespace)'
        method_string = assembler_bad._Assembler__skesa_string()
        assert skesa_str_bad != method_string

    # Test for skesa function with incorrect parameters
    def test_skesa_func_badparams(self):
        skesa_str_test = 'skesa --incorrect params'
        with pytest.raises(subprocess.CalledProcessError):
            assert assembler_good._Assembler__skesa_func(skesa_str_test)

    # Test for skesa function with very small fastq file (which should fail)
    def test_skesa_func_badfile(self):
        skesa_str_bad = 'skesa --fastq ' + forward_bad + ' --use_paired_ends'
        with pytest.raises(subprocess.CalledProcessError):
            assert assembler_bad._Assembler__skesa_func(skesa_str_bad)

    # Test for skesa function when skesa isn't installed
    def test_skesa_func_badcommand(self):
        skesa_str_test = 'conda deactivate && skesa -h'
        with pytest.raises(subprocess.CalledProcessError):
            assert assembler_good._Assembler__skesa_func(skesa_str_test)

    # Test for skesa function with real fastq files
    def test_skesa_func_good(self):
        method_rc = assembler_good._Assembler__skesa_func(skesa_str_good)
        assert skesa_func_good_rc == method_rc

    # Test for Assembler class method integrating all methods
    def test_perform_assembly_good(self):
        skesa_output_string = 'SKESA assembled reads and log files written ' + \
            'to output directory. Return code ' + str(skesa_func_good_rc)
        method_string = assembler_good.perform_assembly()
        assert skesa_output_string == method_string

    # Test for failed integrating method
    def test_perform_assembly_bad(self):
        with pytest.raises(subprocess.CalledProcessError):
            assert assembler_bad.perform_assembly()
