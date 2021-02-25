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
import pytest
import numpy as np


class TestMachineLearningEvaluator:

    def test_evaluate_probability(self):
        """
        Tests the ability to evaluate a good or bad assembly.
        """

        # Evaluating very bad assembly
        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(788, 4029, 4000, 195, 600, 0.66, 2475580)
        species = Species("Actinobacteria bacterium", 1.0)

        evaluator = MachineLearningEvaluator(species, assembly_quality)
        evaluation = evaluator.evaluate()

        assert not evaluation.success
        assert(evaluation.report == "The probability of the assembly being a good assembly is: 0.0.")

        # Evaluating fairly bad assembly
        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(42, 133891, 4000, 6, 600, 0.383, 1986343)
        species = Species("Streptococcus pyogenes", 1.0)

        evaluator = MachineLearningEvaluator(species, assembly_quality)
        evaluation = evaluator.evaluate()

        assert not evaluation.success
        assert(evaluation.report == "The probability of the assembly being a good assembly is: 0.23.")

        # Evaluating fairly good assembly
        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(157, 20000, 4000, 14, 600, 0.311, 1993406)
        species = Species("Campylobacter coli", 1.0)

        evaluator = MachineLearningEvaluator(species, assembly_quality)
        evaluation = evaluator.evaluate()

        assert evaluation.success
        assert(evaluation.report == "The probability of the assembly being a good assembly is: 0.58.")

        # Evaluating very good assembly
        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(19, 481968, 4000, 3, 600, 0.379, 2877876)
        species = Species("Listeria monocytogenes", 1.0)

        evaluator = MachineLearningEvaluator(species, assembly_quality)
        evaluation = evaluator.evaluate()

        assert evaluation.success
        assert(evaluation.report == "The probability of the assembly being a good assembly is: 0.95.")

    def test_missing_genomic_attributes(self):
        """
        Tests machine learning evaluator with missing genomic attributes.
        """

        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(np.nan, 4029, 4000, 195, 600, 0.66, 2475580)
        species = Species("Listeria monocytogenes", 1.0)
        evaluator = MachineLearningEvaluator(species, assembly_quality)
        with pytest.raises(ValueError):
            evaluator.evaluate()

    def test_invalid_genomic_attributes(self):
        """
        Tests machine learning evaluator with numerically incompatible genomic attributes.
        """

        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(0, 0, 4000, 0, 600, 0, 0)
        species = Species("Listeria monocytogenes", 1.0)
        evaluator = MachineLearningEvaluator(species, assembly_quality)
        with pytest.raises(ValueError):
            evaluator.evaluate()
