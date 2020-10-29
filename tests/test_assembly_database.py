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

        assert database.get_n50_quantile(SPECIES, 0.05) == 32344
        assert database.get_n50_quantile(SPECIES, 0.20) == 91861
        assert database.get_n50_quantile(SPECIES, 0.80) == 371530
        assert database.get_n50_quantile(SPECIES, 0.95) == 1055547

        assert database.get_contig_quantile(SPECIES, 0.05) == 12
        assert database.get_contig_quantile(SPECIES, 0.20) == 26
        assert database.get_contig_quantile(SPECIES, 0.80) == 86
        assert database.get_contig_quantile(SPECIES, 0.95) == 227

        assert database.get_l50_quantile(SPECIES, 0.05) == 2
        assert database.get_l50_quantile(SPECIES, 0.20) == 3
        assert database.get_l50_quantile(SPECIES, 0.80) == 10
        assert database.get_l50_quantile(SPECIES, 0.95) == 27

        assert database.get_length_quantile(SPECIES, 0.05) == 2706770
        assert database.get_length_quantile(SPECIES, 0.20) == 2763701
        assert database.get_length_quantile(SPECIES, 0.80) == 2886993
        assert database.get_length_quantile(SPECIES, 0.95) == 2945015

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
