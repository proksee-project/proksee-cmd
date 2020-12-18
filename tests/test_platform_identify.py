'''
Copyright:

University of Manitoba & National Microbiology Laboratory, Canada, 2020

Written by: Arnab Saha Mandal

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
'''

import os
from pathlib import Path

# Importing PlatformIdentifier class from platform_identify.py
from proksee.platform_identify import PlatformIdentifier
import gzip

from proksee.reads import Reads

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))

# Using real fastq files from illumina public data
forward1 = os.path.join(TEST_INPUT_DIR, 'NA12878_fwd.fastq')
reverse1 = os.path.join(TEST_INPUT_DIR, 'NA12878_rev.fastq')
reads1 = Reads(forward1, reverse1)

# Using a real pacbio fastq file and another customized fastq file
forward2 = os.path.join(TEST_INPUT_DIR, 'ATCC_MSA-1003_16S_5reads.fastq.gz')
reverse2 = os.path.join(TEST_INPUT_DIR, 'genuine.fastq')
reads2 = Reads(forward2, reverse2)

# Declaring two instances of PlatformIdentifier class
platform_object1 = PlatformIdentifier(reads1)
platform_object2 = PlatformIdentifier(reads2)

# Declaring another instance of PlatformIdenfity class with forward only
platform_object3 = PlatformIdentifier(Reads(forward2, None))

# Declaring illumina specific true and false snippet files
illum1 = os.path.join(TEST_INPUT_DIR, 'NA12878_illuminatruesnippet.fastq')
illum2 = os.path.join(TEST_INPUT_DIR, 'NA12878_illuminatamperedsnippet1.fastq')
illum3 = os.path.join(TEST_INPUT_DIR, 'NA12878_illuminatamperedsnippet2.fastq')

# Declaring two instances of PlatformIdentifier class with illumina snippet files
platform_object4 = PlatformIdentifier(Reads(illum1, illum2))
platform_object5 = PlatformIdentifier(Reads(illum2, illum3))


class TestPlatIden():

    # Test for checking platform identify method
    def test_platform_identify1(self):
        o1 = open(forward1, 'r')
        o2 = open(reverse1, 'r')
        platform = 'Illumina'
        method_fwd_plat = platform_object1._PlatformIdentifier__plat_iden(o1)
        method_rev_plat = platform_object1._PlatformIdentifier__plat_iden(o2)
        assert platform == method_fwd_plat == method_rev_plat

    # Test for checking platform dictionary method
    def test_platform_output1(self):
        platform_dicn = {forward1: 'Illumina', reverse1: 'Illumina'}
        method_platform = platform_object1._PlatformIdentifier__platform_output()
        assert platform_dicn == method_platform

    # Test for PlatformIdentifier class method integrating all methods
    def test_identify_platform1(self):
        output_string_good = 'Illumina'
        method_string = platform_object1.identify()
        assert output_string_good == method_string

    # Repeating previous three test blocks for second object
    def test_platform_identify2(self):
        o1 = gzip.open(forward2, 'rt')
        o2 = open(reverse2, 'r')
        platform_f = 'Pacbio'
        platform_r = 'Unidentifiable'
        method_fwd_plat = platform_object2._PlatformIdentifier__plat_iden(o1)
        method_rev_plat = platform_object2._PlatformIdentifier__plat_iden(o2)
        assert platform_f == method_fwd_plat
        assert platform_r == method_rev_plat

    def test_platform_output2(self):
        platform_dicn = {forward2: 'Pacbio', reverse2: 'Unidentifiable'}
        method_platform = platform_object2._PlatformIdentifier__platform_output()
        assert platform_dicn == method_platform

    def test_identify_platform2(self):
        output_string_good = 'Pacbio/Unidentifiable'
        method_string = platform_object2.identify()
        assert output_string_good == method_string

    # Test for integrating method for second forward read and no reverse
    def test_identify_platform3(self):
        output_string_good = 'Pacbio'
        method_string = platform_object3.identify()
        assert output_string_good == method_string

    # Tests for integrating method for good and bad illumina snippets
    def test_identify_platform4(self):
        output_string_good = 'Illumina/Unidentifiable'
        method_string = platform_object4.identify()
        assert output_string_good == method_string

    def test_identify_platform5(self):
        output_string_good = 'Unidentifiable'
        method_string = platform_object5.identify()
        assert output_string_good == method_string
