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

from proksee.parser.refseq_masher_parser import parse_species_from_refseq_masher
from proksee.species_estimator import estimate_species_from_estimations, SpeciesEstimator


class TestSkesaAssembler:

    def test_species_estimation(self):
        """
        Tests the estimation of species from estimations (objects).
        """

        valid_masher_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "rs_masher_no_subspecies_column.tab")

        estimations = parse_species_from_refseq_masher(valid_masher_filename)
        species_list = estimate_species_from_estimations(estimations, 0.9, 0.9, 5, ignore_viruses=True)

        assert len(species_list) == 1

        species = species_list[0]

        assert species.name == "Listeria monocytogenes"
        assert species.confidence == 1

    def test_all_species_estimation(self):
        """
        Tests the estimation of all species. In particular, low abundance species estimations.
        """

        input_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "staph_mini.fastq")
        output_directory = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "temp")

        estimator = SpeciesEstimator([input_filename], output_directory)
        species_list = estimator.estimate_all_species()

        top_species = species_list[0]

        assert top_species.name == "Staphylococcus aureus"
        assert top_species.confidence == pytest.approx(1-6.548889999999999e-74, 0.0001)

        bottom_species = species_list[len(species_list) - 1]

        assert bottom_species.name == "Paenibacillus sp. HGF7"
        assert bottom_species.confidence == pytest.approx(1-0.00036287, 0.0001)
