
import os
from pathlib import Path

# Importing OrganismDetection class from organism_detection.py
from proksee.organism_detection import OrganismDetection
import pytest
import subprocess

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))
TEST_OUTPUT_DIR = '{}/data/testout'.format(str(START_DIR))

# Specifying single read fastq with latter being truncated
forward_good = os.path.join(TEST_INPUT_DIR, 'SRR7947278_100kpair_reads.fastq')
forward_bad = os.path.join(TEST_INPUT_DIR, 'SRR7947278_5pair_reads.fastq')

# Declaring instances of OrganismDetection class
organism_identify_good = OrganismDetection(forward_good, None, TEST_OUTPUT_DIR)
organism_identify_bad = OrganismDetection(forward_bad, None, TEST_OUTPUT_DIR)

# Defining variables for successful executions of OrganismDetection modules
refseq_string_good = 'refseq_masher matches ' + forward_good
refseq_func_good_rc = 0
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
        method_tuple = organism_identify_good._OrganismDetection__refseq_masher_func(refseq_string_good)
        refseq_func_tuple = (refseq_out_good, refseq_func_good_rc)
        assert refseq_func_tuple == method_tuple

    # Test for expected major organism
    def test_identify_organism_good(self):
        method_string = organism_identify_good._OrganismDetection__identify_organism(refseq_out_good)
        expected_string = 'Escherichia coli (probability : 1.0), '
        assert expected_string == method_string

    # Test for identifying major organism from incorrect intermediate file
    def test_identify_organism_invalid(self):
        refseq_out_bad = os.path.join(TEST_INPUT_DIR, 'ramdom1')
        with pytest.raises(Exception):
            assert organism_identify_good._OrganismDetection__identify_organism(refseq_out_bad)

    # Idenfying major organism from custom file with one organism as output
    def test_identify_organism_drafted_solo(self):
        refseq_out_bad = os.path.join(TEST_INPUT_DIR, 'refseq_fancysnakes1.out')
        method_string = organism_identify_good._OrganismDetection__identify_organism(refseq_out_bad)
        expected_string = 'Asmodeus Poisonteeth (probability : 0.29), '
        assert expected_string == method_string

    # Identifying major organism from custom file with two organisms as output
    def test_identify_organism_drafted_tie(self):
        refseq_out_bad = os.path.join(TEST_INPUT_DIR, 'refseq_fancysnakes2.out')
        method_string = organism_identify_good._OrganismDetection__identify_organism(refseq_out_bad)
        expected_string = 'Madame White (probability : 0.22), Master Viper (probability : 0.22), '
        assert expected_string == method_string

    # Test for OrganismDetection class method integrating all methods
    def test_major_organism_good(self):
        refseq_output_string = 'Major reference organism is/are Escherichia coli ' + \
            '(probability : 1.0), . Return code ' + str(refseq_func_good_rc)
        method_string = organism_identify_good.major_organism()
        assert refseq_output_string == method_string

    # Test for failed integrating method
    def test_major_organism_bad(self):
        with pytest.raises(subprocess.CalledProcessError):
            assert organism_identify_bad.major_organism()
