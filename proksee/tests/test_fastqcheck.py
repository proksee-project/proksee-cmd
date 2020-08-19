import sys
import os
from pathlib import Path
from proksee.utilities import FastqCheck

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))

# forward and reverse should be a list of multiple possibilities
forward_good = os.path.join(TEST_INPUT_DIR, 'genuine.fastq')
reverse_good = os.path.join(TEST_INPUT_DIR, 'genuine.fastq')

forward_bad1 = os.path.join(TEST_INPUT_DIR, 'fake1.fastq')
reverse_bad1 = os.path.join(TEST_INPUT_DIR, 'fake2.fastq')

forward_bad2 = os.path.join(TEST_INPUT_DIR, 'random1.txt')
reverse_bad2 = os.path.join(TEST_INPUT_DIR, 'random2.txt')

forward_bad3 = os.path.join(TEST_INPUT_DIR, 'winnipeg1.jpg')
reverse_bad3 = os.path.join(TEST_INPUT_DIR, 'winnipeg2.jpg')

forward_bad4 = os.path.join(TEST_INPUT_DIR, 'does_not_exist.fastq.gz')
reverse_bad4 = os.path.join(TEST_INPUT_DIR, 'does_not_exist.fastq')

fastq_object_good = FastqCheck(forward_good, reverse_good)

dicn_good = {forward_good: 1, reverse_good: 1}
status_dicn_good = {forward_good: True, reverse_good: True}
output_tuple_good = ('Read/s is/are valid fastq files..proceeding..', True)


def test_fastq_extn_check():
    method_extn_chk = fastq_object_good._FastqCheck__fastq_extn_check()
    assert dicn_good == method_extn_chk


def test_fastq_line_check():
    o1 = open(forward_good, 'r')
    o2 = open(reverse_good, 'r')
    method_o1 = fastq_object_good._FastqCheck__fastq_line_check(o1)
    method_o2 = fastq_object_good._FastqCheck__fastq_line_check(o2)
    assert method_o1
    assert method_o2


def test_fastq_status_check():
    method_status_chk = fastq_object_good._FastqCheck__fastq_status(dicn_good)
    assert status_dicn_good == method_status_chk


def test_fastq_input_check():
    method_output_tuple = fastq_object_good.fastq_input_check()
    assert output_tuple_good == method_output_tuple