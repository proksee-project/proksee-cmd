import sys
import os
from pathlib import Path
from proksee.organism_detection import OrganismDetection

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))
TEST_OUTPUT_DIR = '{}/data/testout'.format(str(START_DIR))

# forward and reverse should be a list of multiple possibilities
forward_good = os.path.join(TEST_INPUT_DIR, 'SRR7947278_100kpair_reads.fastq')
reverse_good = None

forward_bad1 = os.path.join(TEST_INPUT_DIR, 'fake1.fastq')
reverse_bad1 = os.path.join(TEST_INPUT_DIR, 'fake2.fastq')

organism_identify_good = OrganismDetection(forward_good, reverse_good, TEST_OUTPUT_DIR)

refseq_string_good = 'refseq_masher matches ' + forward_good
refseq_func_good_rc = 0
refseq_out_good = os.path.join(TEST_OUTPUT_DIR, 'refseq.out')


def test_refseq_string():
    method_string = organism_identify_good._OrganismDetection__refseq_masher_string()
    assert refseq_string_good == method_string


def test_refseq_func():
    method_tuple = organism_identify_good._OrganismDetection__refseq_masher_func(refseq_string_good)
    refseq_func_tuple = (refseq_out_good, refseq_func_good_rc)
    assert refseq_func_tuple == method_tuple


def test_identify_organism():
    method_string = organism_identify_good._OrganismDetection__identify_organism(refseq_out_good)
    expected_string = 'Escherichia coli (probability : 1.0), '
    assert expected_string == method_string

