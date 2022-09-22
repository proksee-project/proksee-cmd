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

from proksee.parser.assembly_quality_parser import parse_assembly_quality_from_quast_report


class TestAssemblyQualityParser:

    def test_valid_quast_file(self):
        """
        Tests the parser with a valid QUAST file.
        """

        valid_quast_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "report.tsv")

        minimum_contig_length = 1000
        assembly_quality = parse_assembly_quality_from_quast_report(valid_quast_filename, minimum_contig_length)

        assert assembly_quality.num_contigs == 1
        assert assembly_quality.minimum_contig_length == minimum_contig_length
        assert assembly_quality.n50 == 1249
        assert assembly_quality.n75 == 1249
        assert assembly_quality.l50 == 1
        assert assembly_quality.l75 == 1

    def test_missing_quast_file(self):
        """
        Tests the parser with a missing file. This should raise a FileNotFound exception.
        """

        missing_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "missing.file")

        with pytest.raises(FileNotFoundError):
            parse_assembly_quality_from_quast_report(missing_filename, 1000)
