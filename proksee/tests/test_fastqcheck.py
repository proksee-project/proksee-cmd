import sys
import os
from pathlib import Path
from proksee.utilities import FastqCheck

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))

# forward and reverse should be a list of multiple possibilities
forward = os.path.join(TEST_INPUT_DIR, 'genuine.fastq')
reverse = os.path.join(TEST_INPUT_DIR, 'genuine.fastq')

fastq_object = FastqCheck(forward, reverse)


def test_fastq_extn_check():
    method_extn_chk = fastq_object._FastqCheck__fastq_extn_check()
    expected_extn_chk = {forward: 1, reverse: 1}
    assert expected_extn_chk == method_extn_chk


def test_fastq_line_check():
    o1 = open(forward, 'r')
    o2 = open(reverse, 'r')
    method_o1 = fastq_object._FastqCheck__fastq_line_check(o1)
    method_o2 = fastq_object._FastqCheck__fastq_line_check(o2)
    assert method_o1
    assert method_o2