"""
Copyright Government of Canada 2022

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

from proksee.parser.prokka_parser import parse_prokka_summary_from_txt


class TestProkkaParser:

    def test_simple(self):
        """
        Tests the parser with a simple, unremarkable input file.
        """

        prokka_txt = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "prokka_normal.txt")

        summary = parse_prokka_summary_from_txt(prokka_txt)

        assert(summary.organism == "Salmonella enterica strain")
        assert(summary.contigs == 231)
        assert(summary.bases == 5060450)
        assert(summary.cds == 4685)
        assert(summary.rRNA == 13)
        assert(summary.tRNA == 88)

    def test_missing(self):
        """
        Tests the parser with when the input file is missing fields.
        """

        prokka_txt = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "prokka_missing.txt")

        summary = parse_prokka_summary_from_txt(prokka_txt)

        assert(summary.organism == "Genus species strain")
        assert(summary.contigs == 1)
        assert(summary.bases == 40)
        assert(summary.cds == 0)
        assert(summary.rRNA == 0)
        assert(summary.tRNA == 0)
