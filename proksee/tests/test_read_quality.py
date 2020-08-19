import sys
import os
from pathlib import Path
from proksee.read_quality import ReadFiltering

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))
TEST_OUTPUT_DIR = '{}/data/testout'.format(str(START_DIR))

# forward and reverse should be a list of multiple possibilities
forward_good = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_fwd.fastq')
reverse_good = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_rev.fastq')

forward_bad1 = os.path.join(TEST_INPUT_DIR, 'fake1.fastq')
reverse_bad1 = os.path.join(TEST_INPUT_DIR, 'fake2.fastq')

read_filtering_good = ReadFiltering(forward_good, reverse_good, TEST_OUTPUT_DIR)

forward_good_filt = os.path.join(TEST_OUTPUT_DIR, 'fwd_filtered.fastq')
reverse_good_filt = os.path.join(TEST_OUTPUT_DIR, 'rev_filtered.fastq')
json_out = os.path.join(TEST_OUTPUT_DIR, 'fastp.json')
html_out = os.path.join(TEST_OUTPUT_DIR, 'fastp.html')

fastp_str_good = 'fastp -i ' + forward_good + ' -I ' + reverse_good + ' -o ' + \
    forward_good_filt + ' -O ' + reverse_good_filt + ' -j ' + json_out + \
    ' -h ' + html_out
fastp_func_good_rc = 0
fastp_output_string = 'FASTP filtered reads written to output directory. Return ' + \
    'code ' + str(fastp_func_good_rc)


def test_fastp_string():
    method_string = read_filtering_good._ReadFiltering__fastp_string()
    assert fastp_str_good == method_string


def test_fastp_func():
    method_rc = read_filtering_good._ReadFiltering__fastp_func(fastp_str_good)
    assert fastp_func_good_rc == method_rc


def test_filter_read():
    method_string = read_filtering_good.filter_read()
    assert fastp_output_string == method_string
