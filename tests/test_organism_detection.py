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

# Importing OrganismDetection class from organism_detection.py
from proksee.organism_detection import OrganismDetection
import pytest
import subprocess

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))
TEST_OUTPUT_DIR = '{}/data/testout'.format(str(START_DIR))

# Specifying paired reads and a single truncated read
forward_good = os.path.join(TEST_INPUT_DIR, 'NA12878_fwd.fastq')
reverse_good = os.path.join(TEST_INPUT_DIR, 'NA12878_fwd.fastq')
forward_bad = os.path.join(TEST_INPUT_DIR, 'SRR7947278_5pair_reads.fastq')

# Declaring instances of OrganismDetection class
organism_identify_good = OrganismDetection(forward_good, reverse_good, TEST_OUTPUT_DIR)
organism_identify_bad = OrganismDetection(forward_bad, None, TEST_OUTPUT_DIR)

# Defining variables for successful executions of OrganismDetection modules
refseq_string_good = 'refseq_masher matches ' + forward_good + ' ' + reverse_good
refseq_out_good = os.path.join(TEST_OUTPUT_DIR, 'refseq.out')


class TestReforg():

    # Test for creating good refseq_masher string
    def test_refseq_string_good(self):
        method_string_good = organism_identify_good._OrganismDetection__refseq_masher_string()
        assert refseq_string_good == method_string_good

    # Test for negating bad refseq_masher string
    def test_refseq_string_bad(self):
        refseq_string_bad = 'refseq_masher matches(deleted whitespace)' + forward_bad
        method_string = organism_identify_bad._OrganismDetection__refseq_masher_string()
        assert refseq_string_bad != method_string

    # Test for refseq_masher function with incorrect parameters
    def test_refseq_func_badparams(self):
        refseq_string_test = 'refseq_masher --incorrect params'
        with pytest.raises(subprocess.CalledProcessError):
            assert organism_identify_good._OrganismDetection__refseq_masher_func(refseq_string_test)

    # Test for failed refseq_masher function with very small fastq file
    def test_refseq_func_badfile(self):
        refseq_string_bad = 'refseq_masher matches' + forward_bad
        with pytest.raises(subprocess.CalledProcessError):
            assert organism_identify_bad._OrganismDetection__refseq_masher_func(refseq_string_bad)

    # Test for refseq_masher function when refseq_masher isn't installed
    def test_refseq_func_badcommand(self):
        refseq_string_test = 'conda deactivate && refseq_masher -h'
        with pytest.raises(subprocess.CalledProcessError):
            assert organism_identify_good._OrganismDetection__refseq_masher_func(refseq_string_test)

    # Test for refseq_masher function with real fastq file
    def test_refseq_func_good(self):
        method_refseq = organism_identify_good._OrganismDetection__refseq_masher_func(refseq_string_good)
        assert refseq_out_good == method_refseq

    # Test for expected major organism
    def test_identify_organism_good(self):
        result = organism_identify_good._OrganismDetection__identify_organism(refseq_out_good)
        expected_string = '[Chirostoma humboldtianum (0.2), Crenimugil crenilabis (0.2),' + \
            ' Choaspes benjaminii (0.2), Engaeus sericatus (0.2),' + ' Euastacus spinifer (0.2)]'
        assert expected_string == str(result)

    # Test for identifying major organism from incorrect intermediate file
    def test_identify_organism_invalid(self):
        refseq_out_bad = os.path.join(TEST_INPUT_DIR, 'random1')
        result = organism_identify_good._OrganismDetection__identify_organism(refseq_out_bad)
        expected_string = '[]'
        assert expected_string == str(result)

    # Idenfying major organism from custom file with one organism as output
    def test_identify_organism_drafted_solo(self):
        refseq_out_bad = os.path.join(TEST_INPUT_DIR, 'refseq_fancysnakes1.out')
        result = organism_identify_good._OrganismDetection__identify_organism(refseq_out_bad)
        expected_string = '[Asmodeus Poisonteeth (0.29)]'
        assert expected_string == str(result)

    # Identifying major organism from custom file with two organisms as output
    def test_identify_organism_drafted_tie(self):
        refseq_out_bad = os.path.join(TEST_INPUT_DIR, 'refseq_fancysnakes2.out')
        result = organism_identify_good._OrganismDetection__identify_organism(refseq_out_bad)
        expected_string = '[Madame White (0.22), Master Viper (0.22)]'
        assert expected_string == str(result)

    # Test for OrganismDetection class method integrating all methods
    def test_major_organism_good(self):
        refseq_output_string = '[Chirostoma humboldtianum (0.2), ' + \
            'Crenimugil crenilabis (0.2), Choaspes benjaminii (0.2), ' + \
            'Engaeus sericatus (0.2), Euastacus spinifer (0.2)]'
        result = organism_identify_good.major_organism()
        assert refseq_output_string == str(result)

    # Test for failed integrating method
    def test_major_organism_bad(self):
        with pytest.raises(subprocess.CalledProcessError):
            assert organism_identify_bad.major_organism()
