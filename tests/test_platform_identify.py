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
from proksee.platform_identify import PlatformIdentifier, Platform

from proksee.reads.reads import Reads

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
        reads = Reads(forward1, reverse1)
        platform_identifier = PlatformIdentifier(reads)
        platform = platform_identifier.identify()

        assert platform == Platform.ILLUMINA

    # Repeating previous three test blocks for second object
    def test_platform_identify2(self):
        reads = Reads(forward2, reverse2)

        platform_identifier = PlatformIdentifier(reads)
        platform = platform_identifier.identify()

        assert platform == Platform.UNIDENTIFIABLE

    # Test for integrating method for second forward read and no reverse
    def test_identify_platform3(self):
        reads = Reads(forward2, None)
        platform_identifier = PlatformIdentifier(reads)
        platform = platform_identifier.identify()

        assert platform == Platform.PAC_BIO

    # Tests for integrating method for good and bad illumina snippets
    def test_identify_platform4(self):
        platform_identifier = PlatformIdentifier(Reads(illum1, illum2))
        platform = platform_identifier.identify()

        assert platform == Platform.UNIDENTIFIABLE

    def test_identify_platform5(self):
        platform_identifier = PlatformIdentifier(Reads(illum2, illum3))
        platform = platform_identifier.identify()

        assert platform == Platform.UNIDENTIFIABLE
