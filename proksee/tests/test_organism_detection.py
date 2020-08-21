import sys
import os
from pathlib import Path
from proksee.organism_detection import OrganismDetection
import pytest
import subprocess


START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))
TEST_OUTPUT_DIR = '{}/data/testout'.format(str(START_DIR))

# forward and reverse should be a list of multiple possibilities
forward_good = os.path.join(TEST_INPUT_DIR, 'SRR7947278_100kpair_reads.fastq')
reverse_good = None

forward_bad = os.path.join(TEST_INPUT_DIR, 'SRR7947278_5pair_reads.fastq')
reverse_bad = None

organism_identify_good = OrganismDetection(forward_good, reverse_good, TEST_OUTPUT_DIR)
organism_identify_bad = OrganismDetection(forward_bad, reverse_bad, TEST_OUTPUT_DIR)

refseq_string_good = 'refseq_masher matches ' + forward_good
refseq_func_good_rc = 0
refseq_out_good = os.path.join(TEST_OUTPUT_DIR, 'refseq.out')


def test_refseq_string_good():
    method_string_good = organism_identify_good._OrganismDetection__refseq_masher_string()
    assert refseq_string_good == method_string_good


def test_refseq_string_bad():
    refseq_string_bad = 'refseq_masher matches(deleted whitespace)' + forward_bad
    method_string = organism_identify_bad._OrganismDetection__refseq_masher_string()
    assert refseq_string_bad != method_string


def test_refseq_func_badparams():
    refseq_string_test = 'refseq_masher --incorrect params'
    with pytest.raises(subprocess.CalledProcessError):
        assert organism_identify_good._OrganismDetection__refseq_masher_func(refseq_string_test)


def test_refseq_func_badfile():
    refseq_string_bad = 'refseq_masher matches' + forward_bad
    with pytest.raises(subprocess.CalledProcessError):
        assert organism_identify_bad._OrganismDetection__refseq_masher_func(refseq_string_bad)


def test_refseq_func_badcommand():
    refseq_string_test = 'conda deactivate && refseq_masher -h'
    with pytest.raises(subprocess.CalledProcessError):
        assert organism_identify_good._OrganismDetection__refseq_masher_func(refseq_string_test)


def test_refseq_func_good():
    method_tuple = organism_identify_good._OrganismDetection__refseq_masher_func(refseq_string_good)
    refseq_func_tuple = (refseq_out_good, refseq_func_good_rc)
    assert refseq_func_tuple == method_tuple


def test_identify_organism_good():
    method_string = organism_identify_good._OrganismDetection__identify_organism(refseq_out_good)
    expected_string = 'Escherichia coli (probability : 1.0), '
    assert expected_string == method_string


def test_identify_organism_invalid():
    refseq_out_bad = os.path.join(TEST_INPUT_DIR, 'ramdom.txt')
    with pytest.raises(Exception):
        assert organism_identify_good._OrganismDetection__identify_organism(refseq_out_bad)


def test_identify_organism_drafted_solo():
    refseq_out_bad = os.path.join(TEST_INPUT_DIR, 'refseq_fancysnakes1.out')
    method_string = organism_identify_good._OrganismDetection__identify_organism(refseq_out_bad)
    expected_string = 'Asmodeus Poisonteeth (probability : 0.29), '
    assert expected_string == method_string


def test_identify_organism_drafted_tie():
    refseq_out_bad = os.path.join(TEST_INPUT_DIR, 'refseq_fancysnakes2.out')
    method_string = organism_identify_good._OrganismDetection__identify_organism(refseq_out_bad)
    expected_string = 'Madame White (probability : 0.22), Master Viper (probability : 0.22), '
    assert expected_string == method_string


def test_major_organism_good():
    refseq_output_string = 'Major reference organism is/are Escherichia coli ' + \
        '(probability : 1.0), . Return code ' + str(refseq_func_good_rc)
    method_string = organism_identify_good.major_organism()
    assert refseq_output_string == method_string


def test_major_organism_bad():
    with pytest.raises(subprocess.CalledProcessError):
        assert organism_identify_bad.major_organism()
