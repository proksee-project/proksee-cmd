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
from proksee.evaluation import AssemblyEvaluation, Evaluation

# NCBI RefSeq exclusion criteria:
# https://www.ncbi.nlm.nih.gov/assembly/help/anomnotrefseq/
REFSEQ_MIN_N50 = 5000
REFSEQ_MAX_L50 = 500
REFSEQ_MAX_CONTIGS = 2000

REFSEQ_MIN_LENGTH = 5000
# Not present in above criteria, but we must evaluate length.
# Length cannot be less than the N50 (5000).


class NCBIAssemblyEvaluator(HeuristicEvaluator):
    """
    A heuristic sequence assembly evaluator that uses NCBI RefSeq exclusion criteria.
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
        Evaluates the quality of the assembly. The quality measurements will be compared against the NCBI
        RefSeq exclusion criteria.

        PARAMETERS:
            assembly_quality (AssemblyQuality): the quality measurements of the assembly
        RETURN
            evaluation (AssemblyEvaluation): an evaluation of the assembly's quality
        """

        return self.evaluate_assembly_from_fallback(assembly_quality)

    def evaluate_assembly_from_fallback(self, assembly_quality):
        """
        Evaluates the quality of the assembly. The quality measurements will be compared against the NCBI
        RefSeq exclusion criteria.

        PARAMETERS:
            assembly_quality (AssemblyQuality): the quality measurements of the assembly

        RETURN
            evaluation (AssemblyEvaluation): an evaluation of the assembly's quality
        """

        n50 = assembly_quality.n50
        num_contigs = assembly_quality.num_contigs_filtered
        l50 = assembly_quality.l50
        length = assembly_quality.length_filtered

        total_success = True  # Whether or not all checks pass.

        if n50 < REFSEQ_MIN_N50:
            success = False
            report = "FAIL: The N50 is smaller than expected: {}. ".format(n50)
            report += "The N50 lower bound is: {}.".format(REFSEQ_MIN_N50)

        else:
            success = True
            report = "PASS: The N50 is acceptable: {}. ".format(n50)
            report += "The N50 lower bound is: {}.".format(REFSEQ_MIN_N50)

        n50_evaluation = Evaluation(success, report)
        total_success = total_success and success

        if num_contigs > REFSEQ_MAX_CONTIGS:
            success = False
            report = "FAIL: The number of contigs is larger than expected: {}. ".format(num_contigs)
            report += "The number of contigs upper bound is: {}.".format(REFSEQ_MAX_CONTIGS)
        else:
            success = True
            report = "PASS: The number of contigs is acceptable: {}. ".format(num_contigs)
            report += "The number of contigs upper bound is: {}.".format(REFSEQ_MIN_N50)

        contigs_evaluation = Evaluation(success, report)
        total_success = total_success and success

        if l50 > REFSEQ_MAX_L50:
            success = False
            report = "FAIL: The L50 is larger than expected: {}. ".format(l50)
            report += "The L50 upper bound is: {}.".format(REFSEQ_MAX_L50)

        else:
            success = True
            report = "PASS: The L50 is acceptable: {}. ".format(l50)
            report += "The L50 upper bound is: {}.".format(REFSEQ_MAX_L50)

        l50_evaluation = Evaluation(success, report)
        total_success = total_success and success

        if length < REFSEQ_MIN_LENGTH:
            success = False
            report = "FAIL: The length is smaller than expected: {}. ".format(length)
            report += "The length lower bound is: {}.".format(REFSEQ_MIN_LENGTH)

        else:
            success = True
            report = "PASS: The length is acceptable: {}. ".format(length)
            report += "The length lower bound is: {}.".format(REFSEQ_MIN_LENGTH)

        length_evaluation = Evaluation(success, report)
        total_success = total_success and success

        full_report = n50_evaluation.report + "\n"
        full_report += contigs_evaluation.report + "\n"
        full_report += l50_evaluation.report + "\n"
        full_report += length_evaluation.report

        species_present = True if self.assembly_database.contains(self.species.name) else False

        assembly_evaluation = AssemblyEvaluation(total_success, species_present,
                                                 n50_evaluation, contigs_evaluation, l50_evaluation, length_evaluation,
                                                 full_report)

        return assembly_evaluation
