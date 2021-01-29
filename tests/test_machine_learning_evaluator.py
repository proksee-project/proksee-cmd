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

from proksee.assembly_quality import AssemblyQuality
from proksee.machine_learning_evaluator import MachineLearningEvaluator
from proksee.species import Species


class TestHeuristicEvaluator:

    def test_evaluate_value(self):
        """
        Tests the ability to evaluate a bad assembly as bad.
        """

        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(1000, 3000, 4000, 500, 600, 0.99, 20000)
        species = Species("Listeria monocytogenes", 1.0)

        evaluator = MachineLearningEvaluator(species, assembly_quality)
        evaluation = evaluator.evaluate()

        assert not evaluation.success
        assert(evaluation.report == "The probability of the assembly being a good assembly is: 0.01.")
