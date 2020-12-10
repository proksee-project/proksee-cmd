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

import os
import subprocess

from proksee.evaluation import AssemblyEvaluation, Evaluation
from proksee.parser.assembly_quality_parser import parse_assembly_quality_from_quast_report


class AssemblyEvaluator:
    """
    A class representing an evaluation tool for evaluating an assembly.

    ATTRIBUTES
        contigs_filename (str): the filename of the contigs
        output_directory (str): the filename of the output directory
        quast_directory (str): the filename of the quast directory, which is a subdirectory of output_directory
    """

    def __init__(self, contigs_filename, output_directory):
        """
        Initializes the AssemblyEvaluator object.

        PARAMETERS
            contigs_filename (str): the filename of the contigs file
            output_directory (str): the filename of the run output directory; note that the QUAST output directory will
                be a subdirectory of this directory
        """

        QUAST_DIRECTORY_NAME = "quast"
        QUAST_REPORT_TSV = "report.tsv"

        self.contigs_filename = contigs_filename
        self.output_directory = output_directory
        self.quast_directory = os.path.join(output_directory, QUAST_DIRECTORY_NAME)
        self.quast_report_filename = os.path.join(self.quast_directory, QUAST_REPORT_TSV)

    def evaluate(self):
        """
        Evaluates the quality of an assembly.

        RETURNS
            assembly_quality (AssemblyQuality): an AssemblyQuality object containing measures of quality for the
                assembly

        POST
            The program QUAST will be run to evaluate the assembly.

            Files quast.out and quast.err will be written in the output directory, containing the program output from
            standard out and standard error, respectively.

            A QUAST output directory will be created as a sub-folder in the output directory and contain several QUAST-
            related files.

            The file located at self.quast_report_filename will contain a QUAST report if execution was successful.
        """

        if not os.path.exists(self.contigs_filename):
            raise FileNotFoundError("File not found: " + self.contigs_filename)

        quast_command = "quast " + self.contigs_filename + " -o " + self.quast_directory
        quast_out = open(os.path.join(self.output_directory, "quast.out"), "w+")
        quast_err = open(os.path.join(self.output_directory, "quast.err"), "w+")

        try:
            subprocess.check_call(quast_command, shell=True, stdout=quast_out, stderr=quast_err)
            print("Evaluated the quality of the assembled contigs.")

            assembly_quality = parse_assembly_quality_from_quast_report(self.quast_report_filename)

        except subprocess.CalledProcessError as error:
            raise error

        quast_out.close()
        quast_err.close()

        return assembly_quality


def evaluate_n50(species, assembly_quality, assembly_database):
    """
    Evaluates the N50 of the passed AssemblyQuality against the assembly statistics for the given species in the
    assembly database.

    PARAMETERS
        assembly_quality (AssemblyQuality): an object representing the quality of an assembly
        assembly_database (AssemblyDatabase): an object containing assembly statistics for various species

    RETURN
        evaluation (Evaluation): an evaluation of the N50 against the assembly database
    """

    n50 = assembly_quality.n50
    low_fail = assembly_database.get_n50_quantile(species.name, 0.05)
    low_warning = assembly_database.get_n50_quantile(species.name, 0.20)
    high_warning = assembly_database.get_n50_quantile(species.name, 0.80)
    high_fail = assembly_database.get_n50_quantile(species.name, 0.95)

    evaluation = evaluate_value("N50", n50, low_fail, low_warning, high_warning, high_fail)

    return evaluation


def evaluate_num_contigs(species, assembly_quality, assembly_database):
    """
    Evaluates the number of contigs of the passed AssemblyQuality against the assembly statistics for the given
    species in the assembly database.

    PARAMETERS
        assembly_quality (AssemblyQuality): an object representing the quality of an assembly
        assembly_database (AssemblyDatabase): an object containing assembly statistics for various species

    RETURN
        evaluation (Evaluation): an evaluation of the number of contigs against the assembly database
    """

    num_contigs = assembly_quality.num_contigs
    low_fail = assembly_database.get_contigs_quantile(species.name, 0.05)
    low_warning = assembly_database.get_contigs_quantile(species.name, 0.20)
    high_warning = assembly_database.get_contigs_quantile(species.name, 0.80)
    high_fail = assembly_database.get_contigs_quantile(species.name, 0.95)

    evaluation = evaluate_value("number of contigs", num_contigs, low_fail, low_warning, high_warning, high_fail)

    return evaluation


def evaluate_l50(species, assembly_quality, assembly_database):
    """
    Evaluates the L50 of the passed AssemblyQuality against the assembly statistics for the given species in the
    assembly database.

    PARAMETERS
        assembly_quality (AssemblyQuality): an object representing the quality of an assembly
        assembly_database (AssemblyDatabase): an object containing assembly statistics for various species

    RETURN
        evaluation (Evaluation): an evaluation of the L50 against the assembly database
    """

    l50 = assembly_quality.l50
    low_fail = assembly_database.get_l50_quantile(species.name, 0.05)
    low_warning = assembly_database.get_l50_quantile(species.name, 0.20)
    high_warning = assembly_database.get_l50_quantile(species.name, 0.80)
    high_fail = assembly_database.get_l50_quantile(species.name, 0.95)

    evaluation = evaluate_value("L50", l50, low_fail, low_warning, high_warning, high_fail)

    return evaluation


def evaluate_length(species, assembly_quality, assembly_database):
    """
    Evaluates the assembly length of the passed AssemblyQuality against the assembly statistics for the given
    species in the assembly database.

    PARAMETERS
        assembly_quality (AssemblyQuality): an object representing the quality of an assembly
        assembly_database (AssemblyDatabase): an object containing assembly statistics for various species

    RETURN
        evaluation (Evaluation): an evaluation of the assembly length against the assembly database
    """

    length = assembly_quality.length
    low_fail = assembly_database.get_length_quantile(species.name, 0.05)
    low_warning = assembly_database.get_length_quantile(species.name, 0.20)
    high_warning = assembly_database.get_length_quantile(species.name, 0.80)
    high_fail = assembly_database.get_length_quantile(species.name, 0.95)

    evaluation = evaluate_value("assembly length", length, low_fail, low_warning, high_warning, high_fail)

    return evaluation


def evaluate_assembly(species, assembly_quality, assembly_database):
    """
    Evaluates the quality of the assembly from the passed AssemblyQuality object. The AssemblyQuality measurements
    will be compared against the assembly statistics for the given species in the assembly database. If the species
    is not present in the database, then it will be compared to fallback values.

    PARAMETERS
        assembly_quality (AssemblyQuality): an object representing the quality of an assembly
        assembly_database (AssemblyDatabase): an object containing assembly statistics for various species

    RETURN
        evaluation (AssemblyEvaluation): an evaluation of the assembly's quality
    """

    if assembly_database.contains(species.name):
        assembly_evaluation = evaluate_assembly_from_database(species, assembly_quality, assembly_database)

    else:
        assembly_evaluation = evaluate_assembly_from_fallback(assembly_quality)

    return assembly_evaluation


def evaluate_assembly_from_database(species, assembly_quality, assembly_database):
    """
    Evaluates the quality of the assembly from the passed AssemblyQuality object. The AssemblyQuality measurements
    will be compared against the assembly statistics for the given species in the assembly database.

    PARAMETERS
        assembly_quality (AssemblyQuality): an object representing the quality of an assembly
        assembly_database (AssemblyDatabase): an object containing assembly statistics for various species

    RETURN
        evaluation (AssemblyEvaluation): an evaluation of the assembly's quality against the assembly database
    """

    n50_evaluation = evaluate_n50(species, assembly_quality, assembly_database)
    contigs_evaluation = evaluate_num_contigs(species, assembly_quality, assembly_database)
    l50_evaluation = evaluate_l50(species, assembly_quality, assembly_database)
    length_evaluation = evaluate_length(species, assembly_quality, assembly_database)

    proceed = n50_evaluation.success and contigs_evaluation.success \
        and l50_evaluation.success and length_evaluation.success

    report = "\n"
    report += n50_evaluation.report
    report += contigs_evaluation.report
    report += l50_evaluation.report
    report += length_evaluation.report

    assembly_evaluation = AssemblyEvaluation(n50_evaluation, contigs_evaluation, l50_evaluation, length_evaluation,
                                             proceed, report)

    return assembly_evaluation


def evaluate_assembly_from_fallback(assembly_quality):
    """
    Evaluates the quality of the assembly from the passed AssemblyQuality object. The AssemblyQuality measurements
    will be compared against fallback values.

    PARAMETERS
        assembly_quality (AssemblyQuality): an object representing the quality of an assembly

    RETURN
        evaluation (AssemblyEvaluation): an evaluation of the assembly's quality
    """

    # Values taken from RefSeq assembly exclusion criteria.
    # https://www.ncbi.nlm.nih.gov/assembly/help/anomnotrefseq/
    MIN_N50 = 5000
    MAX_L50 = 500
    MAX_CONTIGS = 2000

    if assembly_quality.n50 < 5000:
        proceed = False
        report = "FAIL: The N50 is smaller than expected: {}\n".format(assembly_quality.n50)
        report += "      The N50 lower bound is: {}\n".format(MIN_N50)

    else:
        proceed = True
        report = "PASS: The N50 is acceptable: {}\n".format(assembly_quality.n50)
        report += "      The N50 lower bound is: {}\n".format(MIN_N50)

    n50_evaluation = Evaluation(proceed, report)

    if assembly_quality.num_contigs > MAX_CONTIGS:
        proceed = False
        report = "FAIL: The number of contigs is larger than expected: {}\n".format(assembly_quality.num_contigs)
        report += "      The number of contigs upper bound is: {}\n".format(MAX_CONTIGS)
    else:
        proceed = True
        report = "PASS: The number of contigs is acceptable: {}\n".format(assembly_quality.num_contigs)
        report += "      The number of contigs lower bound is: {}\n".format(MIN_N50)

    contigs_evaluation = Evaluation(proceed, report)

    if assembly_quality.l50 > MAX_L50:
        proceed = False
        report = "FAIL: The L50 is larger than expected: {}\n".format(assembly_quality.l50)
        report += "      The L50 upper bound is: {}\n".format(MAX_L50)

    else:
        proceed = True
        report = "PASS: The L50 is acceptable: {}\n".format(assembly_quality.l50)
        report += "      The L50 upper bound is: {}\n".format(MAX_L50)

    l50_evaluation = Evaluation(proceed, report)

    report = "\nWARNING: No assembly statistics available for the species!\n\n"
    report += n50_evaluation.report
    report += contigs_evaluation.report
    report += l50_evaluation.report

    assembly_evaluation = AssemblyEvaluation(n50_evaluation, contigs_evaluation, l50_evaluation, None,
                                             proceed, report)

    return assembly_evaluation


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
        report += "FAIL: The {} is smaller than expected: {}\n".format(measurement, value)
        report += "      The {} lower bound is: {}\n".format(measurement, low_fail)

    # (low_fail, low_warning] -> low warning
    elif value <= low_warning:
        success = True
        report += "WARNING: The {} is somewhat smaller than expected: {}\n".format(measurement, value)
        report += "         The {} lower bound is: {}\n".format(measurement, low_fail)

    # (low_warning, high_warning) -> acceptable, no warning
    elif value < high_warning:
        success = True
        report += "PASS: The {} is comparable to similar assemblies: {}\n".format(measurement, value)
        report += "      The acceptable {} range is: ({}, {})\n".format(measurement, low_fail, high_fail)

    # [high_warning, high_fail) -> high warning
    elif value < high_fail:
        success = True
        report += "WARNING: The {} is somewhat larger than expected: {}\n".format(measurement, value)
        report += "         The {} upper bound is: {}\n".format(measurement, high_fail)

    # [high_fail, +infinity) -> high failure
    elif value >= high_fail:
        success = False
        report += "FAIL: The {} is larger than expected: {}\n".format(measurement, value)
        report += "      The {} upper bound is: {}\n".format(measurement, high_fail)

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
    report += "Length: {}\n".format(assembly_quality2.length - assembly_quality1.length)
    report += "\n"

    return report
