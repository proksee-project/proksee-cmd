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
import shutil

import pytest

from proksee.parser.fasta_parser import split_multi_fasta_into_fasta


class TestFastaParser:

    def test_single_contig_fasta_file(self):
        """
        Tests the parser with a valid single-contig FASTA file.
        """

        multi_contig_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "small_single_contig.fasta")
        output_directory = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "temp")

        files_list = split_multi_fasta_into_fasta(multi_contig_filename, output_directory)

        assert len(files_list) == 1
        assert os.path.isfile(os.path.join(output_directory, "0.fasta"))

    def test_multi_contig_fasta_file(self):
        """
        Tests the parser with a valid multi-contig FASTA file.
        """

        multi_contig_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "small_multi_contig.fasta")
        output_directory = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "temp")

        files_list = split_multi_fasta_into_fasta(multi_contig_filename, output_directory)

        assert len(files_list) == 2
        assert os.path.isfile(os.path.join(output_directory, "0.fasta"))
        assert os.path.isfile(os.path.join(output_directory, "1.fasta"))

    def test_missing_fasta_file(self):
        """
        Tests the parser with a missing file. This should raise a FileNotFound exception.
        """

        missing_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "missing.file")
        output_directory = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "temp")

        with pytest.raises(FileNotFoundError):
            split_multi_fasta_into_fasta(missing_filename, output_directory)

    def test_missing_output_directory(self):
        """
        Tests when the output directory is missing and needs to be created.
        """

        multi_contig_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "small_single_contig.fasta")
        output_directory = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "temp")

        # Remove directory if it exists:
        if os.path.isdir(output_directory):
            shutil.rmtree(output_directory)

        files_list = split_multi_fasta_into_fasta(multi_contig_filename, output_directory)

        assert len(files_list) == 1
        assert os.path.isfile(os.path.join(output_directory, "0.fasta"))
