import sys
import os
from pathlib import Path
from proksee.platform_identify import PlatformIdentify
import gzip

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))

# forward and reverse reads from Illumina
forward1 = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_fwd.fastq')
reverse1 = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_rev.fastq')
platform_object1 = PlatformIdentify(forward1, reverse1)


def test_platform_identify1():
    o1 = open(forward1, 'r')
    o2 = open(reverse1, 'r')
    platform = 'Illumina'
    method_fwd_plat = platform_object1._PlatformIdentify__plat_iden(o1)
    method_rev_plat = platform_object1._PlatformIdentify__plat_iden(o2)
    assert platform == method_fwd_plat == method_rev_plat


def test_platform_output1():
    file_dicn = {forward1: 1, reverse1: 1}
    platform_dicn = {forward1: 'Illumina', reverse1: 'Illumina'}
    method_platform = platform_object1._PlatformIdentify__platform_output(file_dicn)
    assert platform_dicn == method_platform


def test_identify_platform1():
    output_string_good = 'Sequencing plaform for NA12878_NextSeq2000_100k_fwd.fastq ' + \
        'and NA12878_NextSeq2000_100k_rev.fastq are same: Illumina'
    method_string = platform_object1.identify_platform()
    assert output_string_good == method_string


# forward read from pacbio and reverse read unidentifiable
forward2 = os.path.join(TEST_INPUT_DIR, 'ATCC_MSA-1003_16S_5reads.fastq.gz')
reverse2 = os.path.join(TEST_INPUT_DIR, 'genuine.fastq')
platform_object2 = PlatformIdentify(forward2, reverse2)


def test_platform_identify2():
    o1 = gzip.open(forward2, 'rt')
    o2 = open(reverse2, 'r')
    platform_f = 'Pacbio' ; platform_r = 'Unidentifiable'
    method_fwd_plat = platform_object2._PlatformIdentify__plat_iden(o1)
    method_rev_plat = platform_object2._PlatformIdentify__plat_iden(o2)
    assert platform_f == method_fwd_plat
    assert platform_r == method_rev_plat


def test_platform_output2():
    file_dicn = {forward2: 0, reverse2: 1}
    platform_dicn = {forward2: 'Pacbio', reverse2: 'Unidentifiable'}
    method_platform = platform_object2._PlatformIdentify__platform_output(file_dicn)
    assert platform_dicn == method_platform


def test_identify_platform2():
    output_string_good = 'Sequencing plaform for ATCC_MSA-1003_16S_5reads.fastq.gz ' + \
        'is Pacbio\nSequencing platform for genuine.fastq is Unidentifiable'
    method_string = platform_object2.identify_platform()
    assert output_string_good == method_string


# Testing public function for reverse being None
platform_object3 = PlatformIdentify(forward2, None)

def test_identify_platform3():
    output_string_good = 'Sequencing plaform for ATCC_MSA-1003_16S_5reads.fastq.gz ' + \
        'is Pacbio'
    method_string = platform_object3.identify_platform()
    assert output_string_good == method_string