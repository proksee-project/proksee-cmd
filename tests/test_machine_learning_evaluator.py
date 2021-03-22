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
from proksee.machine_learning_assembly_qc import NormalizedDatabase
import pytest
import math


class TestMachineLearningEvaluator:

    def test_evaluate_probability(self):
        """
        Tests the ability to evaluate a good or bad assembly.
        """

        # Evaluating very bad assembly
        num_contigs = 788
        n50 = 4029
        n75 = 4000
        l50 = 195
        l75 = 600
        gc_content = 0.66
        length = 2475580
        assembly_quality = AssemblyQuality(num_contigs, n50, n75, l50, l75, gc_content, length)
        species = Species("Actinobacteria bacterium", 1.0)
        normalized_database = NormalizedDatabase(
            species, n50, num_contigs, l50, length, gc_content
        )

        evaluator = MachineLearningEvaluator(species, assembly_quality, normalized_database)
        evaluation = evaluator.evaluate()

        assert not evaluation.success
        assert(evaluation.report == "The probability of the assembly being a good assembly is: 0.0.")

        # Evaluating fairly bad assembly
        num_contigs = 42
        n50 = 133891
        n75 = 4000
        l50 = 6
        l75 = 600
        gc_content = 0.383
        length = 1986343
        assembly_quality = AssemblyQuality(num_contigs, n50, n75, l50, l75, gc_content, length)
        species = Species("Streptococcus pyogenes", 1.0)
        normalized_database = NormalizedDatabase(
            species, n50, num_contigs, l50, length, gc_content
        )

        evaluator = MachineLearningEvaluator(species, assembly_quality, normalized_database)
        evaluation = evaluator.evaluate()

        assert not evaluation.success
        assert(evaluation.report == "The probability of the assembly being a good assembly is: 0.09.")

        # Evaluating fairly good assembly
        num_contigs = 35
        n50 = 41086
        n75 = 4000
        l50 = 5
        l75 = 600
        gc_content = 0.521
        length = 4689259
        assembly_quality = AssemblyQuality(num_contigs, n50, n75, l50, l75, gc_content, length)
        species = Species("Salmonella enterica", 1.0)
        normalized_database = NormalizedDatabase(
            species, n50, num_contigs, l50, length, gc_content
        )

        evaluator = MachineLearningEvaluator(species, assembly_quality, normalized_database)
        evaluation = evaluator.evaluate()

        assert evaluation.success
        assert(evaluation.report == "The probability of the assembly being a good assembly is: 0.54.")

        # Evaluating very good assembly
        num_contigs = 19
        n50 = 481968
        n75 = 4000
        l50 = 3
        l75 = 600
        gc_content = 0.379
        length = 2877876
        assembly_quality = AssemblyQuality(num_contigs, n50, n75, l50, l75, gc_content, length)
        species = Species("Listeria monocytogenes", 1.0)
        normalized_database = NormalizedDatabase(
            species, n50, num_contigs, l50, length, gc_content
        )

        evaluator = MachineLearningEvaluator(species, assembly_quality, normalized_database)
        evaluation = evaluator.evaluate()

        assert evaluation.success
        assert(evaluation.report == "The probability of the assembly being a good assembly is: 0.92.")

    def test_missing_genomic_attributes(self):
        """
        Tests machine learning evaluator with missing genomic attributes.
        """

        num_contigs = 400
        n50 = 4029
        n75 = 4000
        l50 = 195
        l75 = 600
        gc_content = math.nan
        length = 2475580
        assembly_quality = AssemblyQuality(num_contigs, n50, n75, l50, l75, gc_content, length)
        species = Species("Listeria monocytogenes", 1.0)
        normalized_database = NormalizedDatabase(
            species, n50, num_contigs, l50, length, gc_content
        )

        evaluator = MachineLearningEvaluator(species, assembly_quality, normalized_database)
        with pytest.raises(ValueError):
            evaluator.evaluate()

    def test_invalid_genomic_attributes(self):
        """
        Tests machine learning evaluator with numerically incompatible genomic attributes.
        """

        num_contigs = 0
        n50 = 0
        n75 = 4000
        l50 = 0
        l75 = 600
        gc_content = 0
        length = 0
        assembly_quality = AssemblyQuality(num_contigs, n50, n75, l50, l75, gc_content, length)
        species = Species("Listeria monocytogenes", 1.0)
        normalized_database = NormalizedDatabase(
            species, n50, num_contigs, l50, length, gc_content
        )

        evaluator = MachineLearningEvaluator(species, assembly_quality, normalized_database)
        with pytest.raises(ValueError):
            evaluator.evaluate()
