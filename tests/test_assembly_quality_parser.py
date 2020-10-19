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

from proksee.parser.assembly_quality_parser import parse_assembly_quality_from_quast_report


class TestAssemblyQualityParser:

    def test_valid_quast_file(self):

        # Create a valid QUAST TSV file
        valid_quast_file = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "report.tsv")

        assembly_quality = parse_assembly_quality_from_quast_report(valid_quast_file)

        assert assembly_quality.num_contigs == 1
        assert assembly_quality.n50 == 1249
        assert assembly_quality.n75 == 1249
        assert assembly_quality.l50 == 1
        assert assembly_quality.l75 == 1
