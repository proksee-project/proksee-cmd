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

import pytest
import os

from proksee.parser.read_quality_parser import parse_read_quality_from_fastp


class TestReadQualityParser:

    def test_valid_fastp_file(self):

        # Create a valid FASTP JSON file
        valid_fastp_file = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "fastp.json")

        read_quality = parse_read_quality_from_fastp(valid_fastp_file)

        assert read_quality.total_reads == 273
        assert read_quality.total_bases == 27098
        assert read_quality.q20_bases == 26725
        assert read_quality.q30_bases == 26193

        assert read_quality.q20_rate == pytest.approx(0.986235, 0.0001)
        assert read_quality.q30_rate == pytest.approx(0.966603, 0.0001)

        assert read_quality.forward_median_length == 99
        assert read_quality.reverse_median_length == 0

        assert read_quality.gc_content == pytest.approx(0.626024, 0.0001)

        print(read_quality)
