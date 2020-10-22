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
from proksee.assembly_database import AssemblyDatabase


class TestAssemblyDatabase:

    def test_valid_database_file(self):
        """
        Tests the database with a valid file.
        """

        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data",
                                     "fake_assembly_data.csv")
        SPECIES = "Staphylococcus aureus"

        database = AssemblyDatabase(DATABASE_PATH)

        assert database.get_n50_mean(SPECIES) == 2000000
        assert database.get_n50_std(SPECIES) == 2000000
        assert database.get_assembly_size_mean(SPECIES) == 2884032
        assert database.get_assembly_size_std(SPECIES) == 250000
        assert database.get_contigs_mean(SPECIES) == 4
        assert database.get_contigs_std(SPECIES) == 3

        return

    def test_missing_database_file(self):
        """
        Tests the database with a missing file.
        """

        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data",
                                     "invalid.filename")

        with pytest.raises(FileNotFoundError):
            AssemblyDatabase(DATABASE_PATH)

        return
