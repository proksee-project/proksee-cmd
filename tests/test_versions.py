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
from pathlib import Path

import proksee.version as version

ENVIRONMENT_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "environment.yml")

class TestVersions:

    def test_versions_match(self):
        """
        Testing to ensure version numbers in the environment.yml and version.py files match.
        """

        # Parse environment file:
        with open(ENVIRONMENT_PATH) as environment_file:

            for line in environment_file:

                if "fastp" in line:
                    fastp_version_yml = line.split("=")[1].strip()
                elif "skesa" in line:
                    skesa_version_yml = line.split("=")[1].strip()
                elif "mash" in line:
                    mash_version_yml = line.split("=")[1].strip()
                elif "quast" in line:
                    quast_version_yml = line.split("=")[1].strip()
                elif "spades" in line:
                    spades_version_yml = line.split("=")[1].strip()

        assert fastp_version_yml == version.FASTP_VERSION
        assert skesa_version_yml == version.SKESA_VERSION
        assert mash_version_yml == version.MASH_VERSION
        assert quast_version_yml == version.QUAST_VERSION
        assert spades_version_yml == version.SPADES_VERSION
