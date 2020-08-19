import sys
import os
from pathlib import Path
from proksee.assembler import Assembler

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))
TEST_OUTPUT_DIR = '{}/data/testout'.format(str(START_DIR))

# forward and reverse should be a list of multiple possibilities
forward_good = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_fwd.fastq')
reverse_good = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_rev.fastq')

forward_bad1 = os.path.join(TEST_INPUT_DIR, 'fake1.fastq')
reverse_bad1 = os.path.join(TEST_INPUT_DIR, 'fake2.fastq')

assembler_good = Assembler(forward_good, reverse_good, TEST_OUTPUT_DIR)

skesa_str_good = 'skesa --fastq ' + forward_good + ',' + reverse_good
skesa_func_good_rc = 0


def test_skesa_string():
    method_string = assembler_good._Assembler__skesa_string()
    assert skesa_str_good == method_string


def test_skesa_func():
    method_rc = assembler_good._Assembler__skesa_func(skesa_str_good)
    assert skesa_func_good_rc == method_rc


def test_filter_read():
    skesa_output_string = 'SKESA assembled reads and log files written to ' + \
        'output directory. Return code ' + str(skesa_func_good_rc)
    method_string = assembler_good.perform_assembly()
    assert skesa_output_string == method_string
