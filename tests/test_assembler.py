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

from proksee.assembler import Assembler
from proksee.reads import Reads
from proksee.skesa_assembler import SkesaAssembler

INPUT_DIR = os.path.join(Path(__file__).parent.absolute(), "data")
OUTPUT_DIR = TEST_INPUT_DIR = os.path.join(Path(__file__).parent.absolute(), "output")


class TestAssembler:

    def test_abstract_methods(self):
        """
        Testing for crashes by simply running the abstract methods.
        The methods contain only "pass" otherwise.
        """

        forward_filename = os.path.join(INPUT_DIR, "NA12878_fwd.fastq")
        reverse_filename = None
        reads = Reads(forward_filename, reverse_filename)

        # Can't instantiate abstract class, need to instantiate subclass:
        assembler = SkesaAssembler(reads, OUTPUT_DIR)

        Assembler.assemble(assembler)
        Assembler.get_contigs_filename(assembler)
