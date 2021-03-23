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

import os
import joblib
from pathlib import Path
import warnings
from proksee.assembly_evaluator import AssemblyEvaluator
from proksee.evaluation import MachineLearningEvaluation
from proksee.machine_learning_assembly_qc import MachineLearningAssemblyQC, NormalizedDatabase

DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database")
MACHINE_LEARNING_MODEL_FILENAME = "random_forest_n50_numcontigs_l50_length_gccontent.joblib"


class MachineLearningEvaluator(AssemblyEvaluator):
    """
    A machine learning-based sequence assembly evaluator.
    """

    def __init__(self, species):
        """
        Initializes the machine learning-based assembly evaluator.

        PARAMETERS:
            species (Species): the biological species
        """

        super().__init__(species)
        self.normalized_database = NormalizedDatabase()

        # Ignore numpy.ufunc warning (mostly benign, see: github.com/numpy/numpy/issues/11788)
        warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
        self.machine_learning_model = joblib.load(os.path.join(DATABASE_PATH, MACHINE_LEARNING_MODEL_FILENAME))

    def evaluate(self, assembly_quality):
        """
        Evaluates the quality of the assembly using a machine learning-based approach.

        PARAMETERS:
            assembly_quality (AssemblyQuality): the quality measurements of the assembly

        RETURN
            evaluation (Evaluation): an evaluation of the assembly's quality
        """

        n50 = assembly_quality.n50
        l50 = assembly_quality.l50
        num_contigs = assembly_quality.num_contigs
        assembly_length = assembly_quality.length
        gc_content = assembly_quality.gc_content

        if self.normalized_database.contains(self.species.name):
            species_present = True
            assembly_qc = MachineLearningAssemblyQC(self.normalized_database, self.machine_learning_model)
            probability = assembly_qc.calculate_probability(self.species.name, n50, num_contigs, l50,
                                                            assembly_length, gc_content)
            success = True if probability > 0.5 else False
            report = "The probability of the assembly being a good assembly is: " + str(probability) + "."

        else:
            species_present = False
            probability = 0.0
            success = False
            report = "The species is not present in the database."

        evaluation = MachineLearningEvaluation(success, report, probability, species_present)

        return evaluation
