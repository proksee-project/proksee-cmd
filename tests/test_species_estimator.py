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

from proksee.parser.refseq_masher_parser import parse_species_from_refseq_masher
from proksee.species_estimator import estimate_major_species


class TestSkesaAssembler:

    def test_major_species_estimation(self):
        """
        Tests the estimation of major species.
        """

        valid_masher_filename = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "rs_masher_good.tab")

        classifications = parse_species_from_refseq_masher(valid_masher_filename)
        species_list = estimate_major_species(classifications, ignore_viruses=True)

        assert len(species_list) == 1

        species = species_list[0]

        assert species.name == "Listeria monocytogenes"
        assert species.confidence == 1
