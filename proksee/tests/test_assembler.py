import sys
import os
from pathlib import Path
from proksee.assembler import Assembler
import pytest
import subprocess

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))
TEST_OUTPUT_DIR = '{}/data/testout'.format(str(START_DIR))

# forward and reverse should be a list of multiple possibilities
forward_good = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_fwd.fastq')
reverse_good = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_rev.fastq')

forward_bad = os.path.join(TEST_INPUT_DIR, 'SRR7947278_5pair_reads.fastq')
reverse_bad = None

assembler_good = Assembler(forward_good, reverse_good, TEST_OUTPUT_DIR)
assembler_bad = Assembler(forward_bad, reverse_bad, TEST_OUTPUT_DIR)

skesa_str_good = 'skesa --fastq ' + forward_good + ',' + reverse_good
skesa_func_good_rc = 0


def test_skesa_string_good():
    method_string_good = assembler_good._Assembler__skesa_string()
    assert skesa_str_good == method_string_good


def test_skesa_string_bad():
    skesa_str_bad = 'skesa --fastq ' + forward_bad + '--use_paired_ends(deleted whitespace)'
    method_string = assembler_bad._Assembler__skesa_string()
    assert skesa_str_bad != method_string


def test_skesa_func_badparams():
    skesa_str_test = 'skesa --incorrect params'
    with pytest.raises(subprocess.CalledProcessError):
        assert assembler_good._Assembler__skesa_func(skesa_str_test)


def test_skesa_func_badfile():
    skesa_str_bad = 'skesa --fastq ' + forward_bad + ' --use_paired_ends'
    with pytest.raises(subprocess.CalledProcessError):
        assert assembler_bad._Assembler__skesa_func(skesa_str_bad)


def test_skesa_func_badcommand():
    skesa_str_test = 'conda deactivate && skesa -h'
    with pytest.raises(subprocess.CalledProcessError):
        assert assembler_good._Assembler__skesa_func(skesa_str_test)


def test_skesa_func_good():
    method_rc = assembler_good._Assembler__skesa_func(skesa_str_good)
    assert skesa_func_good_rc == method_rc


def test_perform_assembly_good():
    skesa_output_string = 'SKESA assembled reads and log files written to ' + \
        'output directory. Return code ' + str(skesa_func_good_rc)
    method_string = assembler_good.perform_assembly()
    assert skesa_output_string == method_string


def test_perform_assembly_bad():
    with pytest.raises(subprocess.CalledProcessError):
        assert assembler_bad.perform_assembly()
