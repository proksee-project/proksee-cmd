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

from proksee.parser.read_quality_parser import parse_read_quality_from_fastp


class TestReadQualityParser:

    # !!!!!
    def test_valid_fastp_file(self):

        # Create a valid FASTP file
        valid_fastp_file = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "fastp.json")

        read_quality = parse_read_quality_from_fastp(valid_fastp_file)

        print(read_quality)
