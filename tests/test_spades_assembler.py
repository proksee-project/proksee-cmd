"""
Copyright Government of Canada 2020

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
import pytest

from pathlib import Path
from proksee.spades_assembler import SpadesAssembler

INPUT_DIR = os.path.join(Path(__file__).parent.absolute(), "data")
OUTPUT_DIR = TEST_INPUT_DIR = os.path.join(Path(__file__).parent.absolute(), "output")


class TestSpadesAssembler:

    def test_assemble_good_reads(self):

        forward_filename = os.path.join(INPUT_DIR, "NA12878_fwd.fastq")
        reverse_filename = None
        contigs_filename = os.path.join(OUTPUT_DIR, "contigs.fasta")

        # Remove previous assembly if it exists:
        if os.path.isfile(contigs_filename):
            os.remove(contigs_filename)

        assembler = SpadesAssembler(forward_filename, reverse_filename, OUTPUT_DIR)
        assembler.assemble()

        # Check that the assembly produced a contigs file.
        assert os.path.isfile(contigs_filename)

    def test_assemble_good_paired_reads(self):

        forward_filename = os.path.join(INPUT_DIR, "NA12878_fwd.fastq")
        reverse_filename = os.path.join(INPUT_DIR, "NA12878_rev.fastq")
        contigs_filename = os.path.join(OUTPUT_DIR, "contigs.fasta")

        # Remove previous assembly if it exists:
        if os.path.isfile(contigs_filename):
            os.remove(contigs_filename)

        assembler = SpadesAssembler(forward_filename, reverse_filename, OUTPUT_DIR)
        assembler.assemble()

        # Check that the assembly produced a contigs file.
        assert os.path.isfile(contigs_filename)

    def test_assemble_missing_reads(self):

        forward_filename = os.path.join(INPUT_DIR, "missing.file")
        reverse_filename = None

        with pytest.raises(FileNotFoundError):
            SpadesAssembler(forward_filename, reverse_filename, OUTPUT_DIR)
