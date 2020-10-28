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

        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                                     "database.csv")
        SPECIES = "Staphylococcus aureus"

        database = AssemblyDatabase(DATABASE_PATH)

        assert database.get_n50_05(SPECIES) == 32344
        assert database.get_n50_20(SPECIES) == 91861
        assert database.get_n50_80(SPECIES) == 371530
        assert database.get_n50_95(SPECIES) == 1055547

        assert database.get_contig_05(SPECIES) == 12
        assert database.get_contig_20(SPECIES) == 26
        assert database.get_contig_80(SPECIES) == 86
        assert database.get_contig_95(SPECIES) == 227

        assert database.get_l50_05(SPECIES) == 2
        assert database.get_l50_20(SPECIES) == 3
        assert database.get_l50_80(SPECIES) == 10
        assert database.get_l50_95(SPECIES) == 27

        assert database.get_length_05(SPECIES) == 2706770
        assert database.get_length_20(SPECIES) == 2763701
        assert database.get_length_80(SPECIES) == 2886993
        assert database.get_length_95(SPECIES) == 2945015

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
