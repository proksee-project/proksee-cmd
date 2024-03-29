"""
Copyright Government of Canada 2021

Written by: Eric Marinier, National Microbiology Laboratory,
            Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import os

from pathlib import Path
from proksee.reads import Reads

INPUT_DIR = os.path.join(Path(__file__).parent.absolute(), "data")


class TestReads:

    def test_get_file_locations_forward(self):
        """
        Tests the get_file_locations() function when there is only forward
        reads.
        """

        forward_filename = os.path.join(INPUT_DIR, "NA12878_fwd.fastq")
        reverse_filename = None
        reads = Reads(forward_filename, reverse_filename)

        expected = [forward_filename]

        assert reads.get_file_locations() == expected

    def test_get_file_locations_paired(self):
        """
        Tests the get_file_locations() function when there is only forward
        reads.
        """

        forward_filename = os.path.join(INPUT_DIR, "NA12878_fwd.fastq")
        reverse_filename = os.path.join(INPUT_DIR, "NA12878_rev.fastq")
        reads = Reads(forward_filename, reverse_filename)

        expected = [forward_filename, reverse_filename]

        assert reads.get_file_locations() == expected
