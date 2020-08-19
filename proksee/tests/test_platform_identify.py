import sys
import os
from pathlib import Path
from proksee.platform_identify import PlatformIdentify

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))

# forward and reverse should be a list of multiple possibilities
forward_good = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_fwd.fastq')
reverse_good = os.path.join(TEST_INPUT_DIR, 'NA12878_NextSeq2000_100k_rev.fastq')

forward_bad1 = os.path.join(TEST_INPUT_DIR, 'fake1.fastq')
reverse_bad1 = os.path.join(TEST_INPUT_DIR, 'fake2.fastq')

platform_object_good = PlatformIdentify(forward_good, reverse_good)

platform_good = 'Illumina'
dicn_good = {forward_good: 1, reverse_good: 1}
platform_output_good = {forward_good: 'Illumina', reverse_good: 'Illumina'}
output_string_good = 'Sequencing plaform for NA12878_NextSeq2000_100k_fwd.fastq ' + \
    'and NA12878_NextSeq2000_100k_rev.fastq are same: Illumina'


def test_platform_identify():
    o1 = open(forward_good, 'r')
    o2 = open(reverse_good, 'r')
    method_fwd_plat = platform_object_good._PlatformIdentify__plat_iden(o1)
    method_rev_plat = platform_object_good._PlatformIdentify__plat_iden(o2)
    assert platform_good == method_fwd_plat == method_rev_plat


def test_platform_output():
    method_platform = platform_object_good._PlatformIdentify__platform_output(dicn_good)
    assert platform_output_good == method_platform


def test_identify_platform():
    method_string = platform_object_good.identify_platform()
    assert output_string_good == method_string
