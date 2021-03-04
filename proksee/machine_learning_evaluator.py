"""
Copyright Government of Canada 2020

Written by:

Arnab Saha Mandal
    University of Manitoba
    National Microbiology Laboratory, Public Health Agency of Canada

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

from proksee.assembly_evaluator import AssemblyEvaluator
from proksee.evaluation import MachineLearningEvaluation
from proksee.machine_learning_assembly_qc import MachineLearningAssemblyQC, NormalizedDatabase


class MachineLearningEvaluator(AssemblyEvaluator):
    """
    A machine learning-based sequence assembly evaluator.
    """

    def __init__(self, species, assembly_quality):
        """
        Initializes the machine learning-based assembly evaluator.

        PARAMETERS:
            species (Species): the biological species
            assembly_quality (AssemblyQuality): the quality measurements of the assembly
        """

        super().__init__(species, assembly_quality)

    def evaluate(self):
        """
        Evaluates the quality of the assembly using a machine learning-based approach.

        RETURN
            evaluation (Evaluation): an evaluation of the assembly's quality
        """
        species = self.species
        n50 = self.assembly_quality.n50
        l50 = self.assembly_quality.l50
        num_contigs = self.assembly_quality.num_contigs
        assembly_length = self.assembly_quality.length
        gc_content = self.assembly_quality.gc_content

        normalized_database = NormalizedDatabase()

        if normalized_database.contains(self.species.name):
            species_present = True
            machine_learning_instance = MachineLearningAssemblyQC(
                normalized_database, species, n50, num_contigs, l50, assembly_length, gc_content
            )
            probability = machine_learning_instance.calculate_probability()
            success = True if probability > 0.5 else False
            report = "The probability of the assembly being a good assembly is: " + str(probability) + "."

        else:
            species_present = False
            probability = 0.0
            success = False
            report = "The species is not present in the database."

        evaluation = MachineLearningEvaluation(success, report, probability, species_present)

        return evaluation
