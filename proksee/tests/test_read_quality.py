import sys
import os
from pathlib import Path
from proksee.read_quality import ReadFiltering
import subprocess
import pytest

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))
TEST_OUTPUT_DIR = '{}/data/testout'.format(str(START_DIR))
JSON = os.path.join(TEST_OUTPUT_DIR, 'fastp.json')
HTML = os.path.join(TEST_OUTPUT_DIR, 'fastp.html')
RETURN_CODE = 0

# Case 1: Tesing for paired reads
forward1 = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_fwd.fastq')
reverse1 = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_rev.fastq')

read_filtering1 = ReadFiltering(forward1, reverse1, TEST_OUTPUT_DIR)

forward1_filt = os.path.join(TEST_OUTPUT_DIR, 'fwd_filtered.fastq')
reverse1_filt = os.path.join(TEST_OUTPUT_DIR, 'rev_filtered.fastq')

fastp_str1 = 'fastp -i ' + forward1 + ' -I ' + reverse1 + ' -o ' + \
    forward1_filt + ' -O ' + reverse1_filt + ' -j ' + JSON + \
    ' -h ' + HTML


def test_fastp_string1_good():
    method_string_good = read_filtering1._ReadFiltering__fastp_string()
    assert fastp_str1 == method_string_good


def test_fastp_string1_bad():
    fastp_str_bad = 'fastp -i ' + forward1
    method_string_good = read_filtering1._ReadFiltering__fastp_string()
    assert fastp_str_bad != method_string_good


def test_fastp_func1_good():
    method_rc = read_filtering1._ReadFiltering__fastp_func(fastp_str1)
    assert RETURN_CODE == method_rc


def test_fastp_func1_badparams():
    fastp_str_bad = 'fastp --incorrect params'
    with pytest.raises(subprocess.CalledProcessError):
        assert read_filtering1._ReadFiltering__fastp_func(fastp_str_bad)


def test_fastp_func1_badcommand():
    fastp_str_bad = 'conda deactivate && fastp -h'
    with pytest.raises(subprocess.CalledProcessError):
        assert read_filtering1._ReadFiltering__fastp_func(fastp_str_bad)


def test_filter_read1_good():
    fastp_output_string_good = 'FASTP filtered reads written to output directory. Return ' + \
        'code ' + str(RETURN_CODE)
    method_string = read_filtering1.filter_read()
    assert fastp_output_string_good == method_string


def test_filter_read1_bad():
    forward_bad = 'does_not_exist.fastq'
    read_filtering_bad = ReadFiltering(forward_bad, None, TEST_OUTPUT_DIR)
    with pytest.raises(subprocess.CalledProcessError):
        assert read_filtering_bad.filter_read()


# Case 1: Tesing for single read
forward2 = os.path.join(TEST_INPUT_DIR, 'ATCC_MSA-1003_16S_5reads.fastq.gz')

read_filtering2 = ReadFiltering(forward2, None, TEST_OUTPUT_DIR)

forward2_filt = os.path.join(TEST_OUTPUT_DIR, 'fwd_filtered.fastq')

fastp_str2 = 'fastp -i ' + forward2 + ' -o ' + forward1_filt + ' -j ' + \
    JSON + ' -h ' + HTML


def test_fastp_string2_good():
    method_string_good = read_filtering2._ReadFiltering__fastp_string()
    assert fastp_str2 == method_string_good


def test_fastp_func2_good():
    method_rc = read_filtering2._ReadFiltering__fastp_func(fastp_str2)
    assert RETURN_CODE == method_rc


def test_filter_read2_good():
    fastp_output_string_good = 'FASTP filtered reads written to output directory. Return ' + \
        'code ' + str(RETURN_CODE)
    method_string = read_filtering2.filter_read()
    assert fastp_output_string_good == method_string
