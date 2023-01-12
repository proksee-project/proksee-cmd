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

from proksee.parser.mash_parser import MashParser
from proksee.species_estimator import estimate_species_from_estimations, SpeciesEstimator

TEST_MASH_DB_FILENAME = os.path.join(Path(__file__).parent.absolute(), "data", "ecoli.msh")
TEST_ID_MAPPING_FILENAME = os.path.join(Path(__file__).parent.absolute(), "data", "test_id_mapping.tab")


class TestSpeciesEstimator:

    def test_species_estimation(self):
        """
        Tests the estimation of species from estimations (objects).
        """

        valid_mash_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "mash_ecoli.o")

        mash_parser = MashParser(TEST_ID_MAPPING_FILENAME)
        estimations = mash_parser.parse_estimations(valid_mash_filename)
        species_list = estimate_species_from_estimations(estimations, 0.9, 0.9, 5, ignore_viruses=True)

        assert len(species_list) == 1

        species = species_list[0]

        assert species.name == "Escherichia coli"
        assert species.confidence >= 0.99

    def test_all_species_estimation(self):
        """
        Tests the estimation of all species. In particular, low abundance species estimations.
        """

        input_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "ecoli_mini.fasta")
        output_directory = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "temp")

        estimator = SpeciesEstimator([input_filename], output_directory,
                                     TEST_MASH_DB_FILENAME, TEST_ID_MAPPING_FILENAME)
        species_list = estimator.estimate_all_species()

        top_species = species_list[0]

        assert top_species.name == "Escherichia coli"
        assert top_species.confidence == pytest.approx(1, 0.0001)

    def test_estimate_long_filepaths(self, caplog):
        """
        Tests the cut off for when the sum of the filepaths to be passed to Mash are too long.
        Expectation is that some will be cut off and the program will continue normally.
        """

        input_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "ecoli_mini.fasta")
        output_directory = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "temp")

        # Creating the estimator with 500 copies of the same input file.
        # This will result in an argument list that is too many characters long. (i.e. >3500)
        estimator = SpeciesEstimator([input_filename] * 500, output_directory,
                                     TEST_MASH_DB_FILENAME, TEST_ID_MAPPING_FILENAME)
        species_list = estimator.estimate_all_species()

        top_species = species_list[0]

        assert top_species.name == "Escherichia coli"
        assert top_species.confidence == pytest.approx(1, 0.0001)
        assert "The length of all contig filepaths to be screened by Mash exceeds acceptable limits." in caplog.text
        assert "Only the largest 219 contigs will be used." in caplog.text
