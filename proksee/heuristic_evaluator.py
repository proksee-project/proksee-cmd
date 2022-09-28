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

from proksee.assembly_evaluator import AssemblyEvaluator
from proksee.evaluation import Evaluation


# An abstract class of an abstract class
class HeuristicEvaluator(AssemblyEvaluator):
    """
    A heuristic sequence assembly evaluator.

    ATTRIBUTES:
        assembly_database (AssemblyDatabase): a database containing assembly statistics for various species
    """

    def __init__(self, species, assembly_database):
        """
        Initializes the heuristic assembly evaluator.

        PARAMETERS:
            species (Species): the biological species
            assembly_database (AssemblyDatabase): a database containing assembly statistics for various species
        """

        super().__init__(species)
        self.assembly_database = assembly_database

    def evaluate_n50(self, assembly_quality):
        """
        Evaluates the N50 against the assembly statistics for the given species in the assembly database.

        PARAMETERS:
            assembly_quality (AssemblyQuality): the quality measurements of the assembly

        RETURN
            evaluation (Evaluation): an evaluation of the N50 against the assembly database
        """

        database = self.assembly_database
        species = self.species

        n50 = assembly_quality.n50
        low_fail = database.get_n50_quantile(species.name, database.LOW_ERROR_QUANTILE)
        low_warning = database.get_n50_quantile(species.name, database.LOW_WARNING_QUANTILE)
        high_warning = database.get_n50_quantile(species.name, database.HIGH_WARNING_QUANTILE)
        high_fail = database.get_n50_quantile(species.name, database.HIGH_ERROR_QUANTILE)

        evaluation = evaluate_value("N50", n50, low_fail, low_warning, high_warning, high_fail)

        return evaluation

    def evaluate_num_contigs(self, assembly_quality):
        """
        Evaluates the number of contigs against the assembly statistics for the given species in the assembly
        database.

        PARAMETERS:
            assembly_quality (AssemblyQuality): the quality measurements of the assembly

        RETURN
            evaluation (Evaluation): an evaluation of the number of contigs against the assembly database
        """

        database = self.assembly_database
        species = self.species

        num_contigs = assembly_quality.num_contigs
        low_fail = database.get_contigs_quantile(species.name, database.LOW_ERROR_QUANTILE)
        low_warning = database.get_contigs_quantile(species.name, database.LOW_WARNING_QUANTILE)
        high_warning = database.get_contigs_quantile(species.name, database.HIGH_WARNING_QUANTILE)
        high_fail = database.get_contigs_quantile(species.name, database.HIGH_ERROR_QUANTILE)

        evaluation = evaluate_value("number of contigs", num_contigs, low_fail, low_warning, high_warning, high_fail)

        return evaluation

    def evaluate_l50(self, assembly_quality):
        """
        Evaluates the L50 against the assembly statistics for the given species in the assembly database.

        PARAMETERS:
            assembly_quality (AssemblyQuality): the quality measurements of the assembly

        RETURN
            evaluation (Evaluation): an evaluation of the L50 against the assembly database
        """

        database = self.assembly_database
        species = self.species

        l50 = assembly_quality.l50
        low_fail = database.get_l50_quantile(species.name, database.LOW_ERROR_QUANTILE)
        low_warning = database.get_l50_quantile(species.name, database.LOW_WARNING_QUANTILE)
        high_warning = database.get_l50_quantile(species.name, database.HIGH_WARNING_QUANTILE)
        high_fail = database.get_l50_quantile(species.name, database.HIGH_ERROR_QUANTILE)

        evaluation = evaluate_value("L50", l50, low_fail, low_warning, high_warning, high_fail)

        return evaluation

    def evaluate_length(self, assembly_quality):
        """
        Evaluates the assembly length against the assembly statistics for the given species in the assembly
        database.

        PARAMETERS:
            assembly_quality (AssemblyQuality): the quality measurements of the assembly

        RETURN
            evaluation (Evaluation): an evaluation of the assembly length against the assembly database
        """

        database = self.assembly_database
        species = self.species

        length = assembly_quality.length_filtered
        low_fail = database.get_length_quantile(species.name, database.LOW_ERROR_QUANTILE)
        low_warning = database.get_length_quantile(species.name, database.LOW_WARNING_QUANTILE)
        high_warning = database.get_length_quantile(species.name, database.HIGH_WARNING_QUANTILE)
        high_fail = database.get_length_quantile(species.name, database.HIGH_ERROR_QUANTILE)

        evaluation = evaluate_value("assembly length", length, low_fail, low_warning, high_warning, high_fail)

        return evaluation


def evaluate_value(measurement, value, low_fail, low_warning, high_warning, high_fail):
    """
    Evaluates a generic value for a measurement and reports whether or not it is within acceptable bounds.

    PARAMETERS
        measurement (str): plain-language name of the measurement (ex: "N50")
        value (comparable): the value to evaluate
        low_fail (comparable): the lower bound of failure
        low_warning (comparable): the lower bound for warning
        high_warning (comparable): the higher bound for warning
        high_fail (comparable): the higher bound of failure

    RETURNS
        evaluation (Evaluation): an evaluation of the measurement against the passed thresholds
    """

    report = ""
    success = False

    # (-infinity, low_fail] -> low failure
    if value <= low_fail:
        success = False
        report += "FAIL: The {} is smaller than expected: {}. ".format(measurement, value)
        report += "The {} lower bound is: {}.".format(measurement, low_fail)

    # (low_fail, low_warning] -> low warning
    elif value <= low_warning:
        success = True
        report += "WARNING: The {} is somewhat smaller than expected: {}. ".format(measurement, value)
        report += "The {} lower bound is: {}.".format(measurement, low_fail)

    # (low_warning, high_warning) -> acceptable, no warning
    elif value < high_warning:
        success = True
        report += "PASS: The {} is comparable to similar assemblies: {}. ".format(measurement, value)
        report += "The acceptable {} range is: ({}, {}).".format(measurement, low_fail, high_fail)

    # [high_warning, high_fail) -> high warning
    elif value < high_fail:
        success = True
        report += "WARNING: The {} is somewhat larger than expected: {}. ".format(measurement, value)
        report += "The {} upper bound is: {}.".format(measurement, high_fail)

    # [high_fail, +infinity) -> high failure
    elif value >= high_fail:
        success = False
        report += "FAIL: The {} is larger than expected: {}. ".format(measurement, value)
        report += "The {} upper bound is: {}.".format(measurement, high_fail)

    evaluation = Evaluation(success, report)

    return evaluation


def compare_assemblies(assembly_quality1, assembly_quality2):
    """
    Compares the quality of one assembly with the quality of another assembly.

    PARAMETERS
        assembly_quality1 (AssemblyQuality): the quality of the first assembly
        assembly_quality2 (AssemblyQuality): the quality of the second assembly

    RETURNS
        report (str): a plain-language text report comparing the quality of one assembly with the other
    """

    report = "Changes in assembly statistics:\n"
    report += "N50: {}\n".format(assembly_quality2.n50 - assembly_quality1.n50)
    report += "Number of Contigs: {}\n".format(assembly_quality2.num_contigs - assembly_quality1.num_contigs)
    report += "L50: {}\n".format(assembly_quality2.l50 - assembly_quality1.l50)
    report += "Length: {}\n".format(assembly_quality2.length_filtered - assembly_quality1.length_filtered)
    report += "\n"

    return report
