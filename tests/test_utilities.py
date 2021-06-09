"""
Copyright Government of Canada 2021

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

from proksee.assembly_database import AssemblyDatabase
from proksee.species import Species
from proksee.utilities import determine_species

INPUT_DIR = os.path.join(Path(__file__).parent.absolute(), "data")
OUTPUT_DIR = os.path.join(Path(__file__).parent.absolute(), "output")
DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database",
                             "refseq_short.csv")

TEST_MASH_DB_FILENAME = os.path.join(Path(__file__).parent.absolute(), "data", "ecoli.msh")
TEST_ID_MAPPING_FILENAME = os.path.join(Path(__file__).parent.absolute(), "data", "test_id_mapping.tab")


class TestUtilities:

    def test_determine_species_provided_present(self):
        """
        Tests when the species name is provided, and is present in the database.
        """

        input_filenames = [os.path.join(INPUT_DIR, "ecoli_mini.fasta")]
        database = AssemblyDatabase(DATABASE_PATH)
        species_name = "Escherichia coli"

        species_list = determine_species(input_filenames, database, OUTPUT_DIR,
                                         TEST_MASH_DB_FILENAME, TEST_ID_MAPPING_FILENAME, species_name)
        assert(species_list[0] == Species("Escherichia coli", 1.0))

    def test_determine_species_provided_absent(self):
        """
        Tests when the species name is provided, but is not present in the database.

        The provided file will be too small to accurately determine the species, so an "Unknown" species will be
        reported.
        """

        input_filenames = [os.path.join(INPUT_DIR, "ecoli_mini.fasta")]
        database = AssemblyDatabase(DATABASE_PATH)
        species_name = "TYPO! Escherichia coli"

        species_list = determine_species(input_filenames, database, OUTPUT_DIR,
                                         TEST_MASH_DB_FILENAME, TEST_ID_MAPPING_FILENAME, species_name)

        print(species_list)

        # Tries to find species when name missing:
        # The problem here, is it will find "Unknown", because the test data file isn't large enough
        # to accurately determine the species.
        assert(species_list[0] == Species("Unknown", 0.0))
