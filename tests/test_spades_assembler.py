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

from proksee.reads import Reads
from proksee.spades_assembler import SpadesAssembler
from proksee.resource_specification import ResourceSpecification

INPUT_DIR = os.path.join(Path(__file__).parent.absolute(), "data")
OUTPUT_DIR = TEST_INPUT_DIR = os.path.join(Path(__file__).parent.absolute(), "output")
RESOURCE_SPECIFICATION = ResourceSpecification(4, 4)  # 4 threads, 4 gigabytes


class TestSpadesAssembler:

    def test_assemble_good_reads(self):
        """
        Tests the SPAdes assembler class when reads are good.
        """

        forward_filename = os.path.join(INPUT_DIR, "NA12878_fwd.fastq")
        reverse_filename = None
        reads = Reads(forward_filename, reverse_filename)

        assembler = SpadesAssembler(reads, OUTPUT_DIR, RESOURCE_SPECIFICATION)
        contigs_filename = assembler.get_contigs_filename()

        # Remove previous assembly if it exists:
        if os.path.isfile(contigs_filename):
            os.remove(contigs_filename)

        assembler.assemble()

        # Check that the assembly produced a contigs file.
        assert os.path.isfile(contigs_filename)

    def test_assemble_good_paired_reads(self):
        """
        Tests the SPAdes assembler class when paired reads are good.
        """

        forward_filename = os.path.join(INPUT_DIR, "NA12878_fwd.fastq")
        reverse_filename = os.path.join(INPUT_DIR, "NA12878_rev.fastq")
        reads = Reads(forward_filename, reverse_filename)

        assembler = SpadesAssembler(reads, OUTPUT_DIR, RESOURCE_SPECIFICATION)
        contigs_filename = assembler.get_contigs_filename()

        # Remove previous assembly if it exists:
        if os.path.isfile(contigs_filename):
            os.remove(contigs_filename)

        assembler.assemble()

        # Check that the assembly produced a contigs file.
        assert os.path.isfile(contigs_filename)

    def test_assemble_missing_reads(self):
        """
        Tests the SPAdes assembler class when reads are missing.
        """

        forward_filename = os.path.join(INPUT_DIR, "missing.file")
        reverse_filename = None
        reads = Reads(forward_filename, reverse_filename)

        with pytest.raises(FileNotFoundError):
            SpadesAssembler(reads, OUTPUT_DIR, RESOURCE_SPECIFICATION)

    def test_bad_file(self):
        """
        Tests that the assembler throws an exception when the file exists, but
        is not appropriate for assembly.

        This should create a SystemExit error, as the CalledProcess error is
        handled by the assembler.
        """

        forward_filename = os.path.join(INPUT_DIR, "winnipeg1.jpg")
        reverse_filename = None
        reads = Reads(forward_filename, reverse_filename)

        assembler = SpadesAssembler(reads, OUTPUT_DIR, RESOURCE_SPECIFICATION)

        with pytest.raises(SystemExit):
            assembler.assemble()
