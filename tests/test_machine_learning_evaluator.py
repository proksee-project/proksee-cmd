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
import math


class TestMachineLearningEvaluator:

    def test_evaluate_probability(self):
        """
        Tests the ability to evaluate a good or bad assembly.
        """

        # Evaluating very bad assembly
        # num_contigs, minimum_contig_length, n50, n75, l50, l75, gc_content, length_unfiltered, length_filtered
        assembly_quality = AssemblyQuality(2806, 1000, 3039, 4000, 522, 600, 0.573, 5208476, 5208476)
        species = Species("Klebsiella pneumoniae", 1.0)

        evaluator = MachineLearningEvaluator(species)
        evaluation = evaluator.evaluate(assembly_quality)

        assert not evaluation.success
        assert (evaluation.report == "The probability of the assembly being similar "
                + "to a curated assembly of the same species: 0.0.")

        # Evaluating fairly bad assembly
        # num_contigs, minimum_contig_length, n50, n75, l50, l75, gc_content, length_unfiltered, length_filtered
        assembly_quality = AssemblyQuality(545295, 1000, 108384, 100000, 6, 8, 0.387, 2117857, 2117857)
        species = Species("Streptococcus pyogenes", 1.0)

        evaluator = MachineLearningEvaluator(species)
        evaluation = evaluator.evaluate(assembly_quality)

        assert not evaluation.success
        assert (evaluation.report == "The probability of the assembly being similar "
                + "to a curated assembly of the same species: 0.24.")

        # Evaluating fairly good assembly
        # num_contigs, minimum_contig_length, n50, n75, l50, l75, gc_content, length_unfiltered, length_filtered
        assembly_quality = AssemblyQuality(35, 1000, 41086, 4000, 5, 600, 0.521, 4689259, 4689259)
        species = Species("Salmonella enterica", 1.0)

        evaluator = MachineLearningEvaluator(species)
        evaluation = evaluator.evaluate(assembly_quality)

        assert evaluation.success
        assert (evaluation.report == "The probability of the assembly being similar "
                + "to a curated assembly of the same species: 0.64.")

        # Evaluating very good assembly
        # num_contigs, minimum_contig_length, n50, n75, l50, l75, gc_content, length_unfiltered, length_filtered
        assembly_quality = AssemblyQuality(36, 1000, 359164, 359200, 3, 4, 0.378, 3094380, 3094380)
        species = Species("Listeria monocytogenes", 1.0)

        evaluator = MachineLearningEvaluator(species)
        evaluation = evaluator.evaluate(assembly_quality)

        assert evaluation.success
        assert (evaluation.report == "The probability of the assembly being similar "
                + "to a curated assembly of the same species: 0.96.")

    def test_missing_genomic_attributes(self):
        """
        Tests machine learning evaluator with missing genomic attributes.
        """

        # num_contigs, minimum_contig_length, n50, n75, l50, l75, gc_content, length_unfiltered, length_filtered
        assembly_quality = AssemblyQuality(400, 1000, 4029, 4000, 195, 600, math.nan, 2475580, 2475580)
        species = Species("Listeria monocytogenes", 1.0)

        evaluator = MachineLearningEvaluator(species)
        with pytest.raises(ValueError):
            evaluator.evaluate(assembly_quality)

    def test_invalid_genomic_attributes(self):
        """
        Tests machine learning evaluator with numerically incompatible genomic attributes.
        """

        # num_contigs, minimum_contig_length, n50, n75, l50, l75, gc_content, length_unfiltered, length_filtered
        assembly_quality = AssemblyQuality(0, 1000, 0, 4000, 0, 600, 0, 0, 0)
        species = Species("Listeria monocytogenes", 1.0)

        evaluator = MachineLearningEvaluator(species)
        with pytest.raises(ValueError):
            evaluator.evaluate(assembly_quality)
