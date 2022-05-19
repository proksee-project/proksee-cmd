"""
Copyright Government of Canada 2022

Written by:

Eric Marinier
    National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from proksee.assemble.assembly_evaluator import AssemblyEvaluator
from proksee.evaluate.evaluation import MachineLearningEvaluation


class MLAnnoatedAssemblyEvaluator(AssemblyEvaluator):
    """
    A machine learning-based sequence assembly evaluator.
    """

    def __init__(self, species):
        """
        Initializes the machine learning-based annoated assembly evaluator.

        PARAMETERS:
            species (Species): the biological species
        """

        super().__init__(species)

    def evaluate(self, assembly_quality, annotation_summary):
        """
        Evaluates the quality of the assembly using a machine learning-based approach.

        PARAMETERS:
            assembly_quality (AssemblyQuality): the quality measurements of the assembly
            annotation_summary (AnnotationSummary): a summary of annotation metrics (related to the assembly)

        RETURN
            evaluation (Evaluation): an evaluation of the assembly's quality
        """

        n50 = assembly_quality.n50
        l50 = assembly_quality.l50
        num_contigs = assembly_quality.num_contigs
        assembly_length = assembly_quality.length
        gc_content = assembly_quality.gc_content

        # TODO: Integrate ML code
        cds = annotation_summary.cds
        tRNA = annotation_summary.tRNA

        # TODO: Temporary!
        if self.species.name:
            species_present = True

            # TODO: Integrate ML code
            # probability = calculate_probability(n50, l50, num_contigs, assembly_length, gc_content, cds, tRNA)
            print([n50, l50, num_contigs, assembly_length, gc_content, cds, tRNA])
            probability = 404

            success = True if probability > 0.5 else False
            report = "The probability of the assembly being a good assembly is: " + str(probability) + "."

        else:
            species_present = False
            probability = 0.0
            success = False
            report = "The species is not present in the database."

        evaluation = MachineLearningEvaluation(success, report, probability, species_present)

        return evaluation
