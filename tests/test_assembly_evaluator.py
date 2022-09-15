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
from proksee.assembly_evaluator import AssemblyEvaluator
from proksee.assembly_quality import AssemblyQuality
from proksee.species import Species
from proksee.species_assembly_evaluator import SpeciesAssemblyEvaluator


class TestAssemblyEvaluator:

    def test_abstract_methods(self):
        """
        Testing for crashes by simply running the abstract methods.
        The methods contain only "pass" otherwise.
        """

        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database",
                                     "refseq_short.csv")
        species = Species("Staphylococcus aureus", 1.0)

        database = AssemblyDatabase(DATABASE_PATH)
        evaluator = SpeciesAssemblyEvaluator(species, database)  # Need to instantiate child class.

        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(788, 4029, 4000, 195, 600, 0.66, 2475580)

        AssemblyEvaluator.evaluate(evaluator, assembly_quality)
