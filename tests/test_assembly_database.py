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

        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database",
                                     "refseq_short.csv")
        SPECIES = "Staphylococcus aureus"

        database = AssemblyDatabase(DATABASE_PATH)

        assert database.get_n50_quantile(SPECIES, 0.05) == 24300.1
        assert database.get_n50_quantile(SPECIES, 0.20) == 73503
        assert database.get_n50_quantile(SPECIES, 0.80) == 329268.4
        assert database.get_n50_quantile(SPECIES, 0.95) == 672271.45

        assert database.get_contigs_quantile(SPECIES, 0.05) == 17
        assert database.get_contigs_quantile(SPECIES, 0.20) == 29
        assert database.get_contigs_quantile(SPECIES, 0.80) == 113
        assert database.get_contigs_quantile(SPECIES, 0.95) == 286.85

        assert database.get_l50_quantile(SPECIES, 0.05) == 2
        assert database.get_l50_quantile(SPECIES, 0.20) == 3
        assert database.get_l50_quantile(SPECIES, 0.80) == 12
        assert database.get_l50_quantile(SPECIES, 0.95) == 34

        assert database.get_length_quantile(SPECIES, 0.05) == 2696014.45
        assert database.get_length_quantile(SPECIES, 0.20) == 2754871.4
        assert database.get_length_quantile(SPECIES, 0.80) == 2886820.4
        assert database.get_length_quantile(SPECIES, 0.95) == 2937730.05

        return

    def test_missing_quantiles(self):
        """
        Tests the database by requesting a missing quantiles.
        """

        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database",
                                     "refseq_short.csv")
        SPECIES = "Staphylococcus aureus"

        database = AssemblyDatabase(DATABASE_PATH)

        assert database.get_n50_quantile(SPECIES, 0.499) is None
        assert database.get_contigs_quantile(SPECIES, 0.501) is None
        assert database.get_l50_quantile(SPECIES, 0.707) is None
        assert database.get_length_quantile(SPECIES, 0.454) is None

    def test_missing_database_file(self):
        """
        Tests the database with a missing file.
        """

        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data",
                                     "invalid.filename")

        with pytest.raises(FileNotFoundError):
            AssemblyDatabase(DATABASE_PATH)

        return

    def test_missing_species(self):
        """
        Tests when the species are missing from the database.
        """

        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database",
                                     "refseq_short.csv")
        SPECIES = "does not exist"

        database = AssemblyDatabase(DATABASE_PATH)

        assert database.get_n50_quantile(SPECIES, 0.05) is None
        assert database.get_contigs_quantile(SPECIES, 0.2) is None
        assert database.get_l50_quantile(SPECIES, 0.8) is None
        assert database.get_length_quantile(SPECIES, 0.95) is None
