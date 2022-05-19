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

from proksee.species.species import Species


class TestSpecies:

    def test_str(self):
        """
        Tests the species __str__() function for correctness.
        """

        species = Species("Listeria monocytogenes", 1.0)
        string = str(species)

        assert string == "Listeria monocytogenes (p=1.00)"

    def test_repr(self):
        """
        Tests the species __repr__() function for correctness.
        """

        species = Species("Listeria monocytogenes", 1.0)
        representation = repr(species)

        assert representation == "Listeria monocytogenes (1.0)"
