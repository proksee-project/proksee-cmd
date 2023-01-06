"""
Copyright Government of Canada 2022

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

from proksee.heuristic_evaluator import HeuristicEvaluator
from proksee.evaluation import AssemblyEvaluation


class SpeciesAssemblyEvaluator(HeuristicEvaluator):
    """
    A heuristic sequence assembly evaluator that uses assembly statistics for a particular species.

    ATTRIBUTES:
        assembly_database (AssemblyDatabase): a database containing assembly statistics for various species
    """

    def __init__(self, species, assembly_database):
        """
        Initializes the assembly evaluator.

        PARAMETERS:
            species (Species): the biological species
            assembly_database (AssemblyDatabase): a database containing assembly statistics for various species
        """

        super().__init__(species, assembly_database)

    def evaluate(self, assembly_quality):
        """
        Evaluates the quality of the assembly. The quality measurements will be compared against the assembly
        statistics for the given species in the assembly database.

        PARAMETERS:
            assembly_quality (AssemblyQuality): the quality measurements of the assembly
        RETURN
            evaluation (AssemblyEvaluation): an evaluation of the assembly's quality
        """

        return self.evaluate_assembly_from_database(assembly_quality)

    def evaluate_assembly_from_database(self, assembly_quality):
        """
        Evaluates the quality of the assembly. The quality measurements will be compared against the assembly
        statistics for the given species in the assembly database.

        RETURN
            evaluation (AssemblyEvaluation): an evaluation of the assembly's quality against the assembly database
        """

        # Species is not in the database:
        if not self.assembly_database.contains(self.species.name):
            return AssemblyEvaluation(False, False, None, None, None, None,
                                      "The species was not found in the database.")

        n50_evaluation = self.evaluate_n50(assembly_quality)
        contigs_evaluation = self.evaluate_num_contigs(assembly_quality)
        l50_evaluation = self.evaluate_l50(assembly_quality)
        length_evaluation = self.evaluate_length(assembly_quality)

        success = n50_evaluation.success and contigs_evaluation.success \
            and l50_evaluation.success and length_evaluation.success

        report = n50_evaluation.report + "\n"
        report += contigs_evaluation.report + "\n"
        report += l50_evaluation.report + "\n"
        report += length_evaluation.report

        assembly_evaluation = AssemblyEvaluation(success, True,
                                                 n50_evaluation, contigs_evaluation, l50_evaluation, length_evaluation,
                                                 report)

        return assembly_evaluation
