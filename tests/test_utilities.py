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


class TestUtilities:

    def test_determine_species_provided_present(self):
        """
        Tests when the species name is provided, and is present in the database.
        """

        input_filenames = [os.path.join(INPUT_DIR, "staph_mini.fastq")]
        database = AssemblyDatabase(DATABASE_PATH)
        species_name = "Staphylococcus aureus"

        species_list = determine_species(input_filenames, database, OUTPUT_DIR, species_name)
        assert(species_list[0] == Species("Staphylococcus aureus", 1.0))

    def test_determine_species_provided_absent(self):
        """
        Tests when the species name is provided, but is not present in the database.
        """

        input_filenames = [os.path.join(INPUT_DIR, "s_pseudointermedius.fasta")]
        database = AssemblyDatabase(DATABASE_PATH)
        species_name = "Staphylococcus pseudintermedius"

        species_list = determine_species(input_filenames, database, OUTPUT_DIR, species_name)

        # Tries to find species when name missing
        assert(species_list[0] == Species("Staphylococcus pseudintermedius", 1.0))
