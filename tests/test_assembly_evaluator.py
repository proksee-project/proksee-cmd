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
import pytest

from proksee.assembly_evaluator import AssemblyEvaluator, evaluate_value


class TestAssemblyEvaluator:

    def test_valid_contig_file(self):
        """
        Tests the AssemblyEvaluator with a valid contig file.
        """

        contigs_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "simple_contig.fasta")
        output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

        # Create a location for output, if it doesn't already exist:
        if not os.path.isdir(output_directory):
            os.mkdir(output_directory)

        assembly_evaluator = AssemblyEvaluator(contigs_filename, output_directory)
        assembly_evaluator.evaluate()

        assert os.path.isfile(assembly_evaluator.quast_report_filename)

    def test_missing_contig_file(self):
        """
        Tests the AssemblyEvaluator with a missing contig file. This should raise a FileNotFound exception.
        """

        missing_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "missing.file")
        output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

        # Create a location for output, if it doesn't already exist:
        if not os.path.isdir(output_directory):
            os.mkdir(output_directory)

        assembly_evaluator = AssemblyEvaluator(missing_filename, output_directory)

        with pytest.raises(FileNotFoundError):
            assembly_evaluator.evaluate()

    def test_evaluate_value(self):
        """
        Tests the expert system's function for evaluating whether or a value is acceptable.
        """

        low_fail = 5
        low_warning = 10
        high_warning = 20
        high_fail = 25

        # fail -- too low
        evaluation = evaluate_value("measurement", 2, low_fail, low_warning, high_warning, high_fail)
        assert not evaluation.success
        expected_report = "FAIL: The measurement is smaller than expected: 2\n"
        expected_report += "      The measurement lower bound is: 5\n"
        assert evaluation.report == expected_report

        # fail -- too low, on threshold
        evaluation = evaluate_value("measurement", 5, low_fail, low_warning, high_warning, high_fail)
        assert not evaluation.success
        expected_report = "FAIL: The measurement is smaller than expected: 5\n"
        expected_report += "      The measurement lower bound is: 5\n"
        assert evaluation.report == expected_report

        # low warning -- above low fail threshold
        evaluation = evaluate_value("measurement", 6, low_fail, low_warning, high_warning, high_fail)
        assert evaluation.success
        expected_report = "WARNING: The measurement is somewhat smaller than expected: 6\n"
        expected_report += "         The measurement lower bound is: 5\n"
        assert evaluation.report == expected_report

        # low warning -- on low warning threshold
        evaluation = evaluate_value("measurement", 10, low_fail, low_warning, high_warning, high_fail)
        assert evaluation.success
        expected_report = "WARNING: The measurement is somewhat smaller than expected: 10\n"
        expected_report += "         The measurement lower bound is: 5\n"
        assert evaluation.report == expected_report

        # acceptable -- above low warning threshold
        evaluation = evaluate_value("measurement", 11, low_fail, low_warning, high_warning, high_fail)
        assert evaluation.success
        expected_report = "PASS: The measurement is comparable to similar assemblies: 11\n"
        expected_report += "      The acceptable measurement range is: (5, 25)\n"
        assert evaluation.report == expected_report

        # acceptable -- typical
        evaluation = evaluate_value("measurement", 15, low_fail, low_warning, high_warning, high_fail)
        assert evaluation.success
        expected_report = "PASS: The measurement is comparable to similar assemblies: 15\n"
        expected_report += "      The acceptable measurement range is: (5, 25)\n"
        assert evaluation.report == expected_report

        # acceptable -- below high warning threshold
        evaluation = evaluate_value("measurement", 19, low_fail, low_warning, high_warning, high_fail)
        assert evaluation.success
        expected_report = "PASS: The measurement is comparable to similar assemblies: 19\n"
        expected_report += "      The acceptable measurement range is: (5, 25)\n"
        assert evaluation.report == expected_report

        # high warning -- on threshold
        evaluation = evaluate_value("measurement", 20, low_fail, low_warning, high_warning, high_fail)
        assert evaluation.success
        expected_report = "WARNING: The measurement is somewhat larger than expected: 20\n"
        expected_report += "         The measurement upper bound is: 25\n"
        assert evaluation.report == expected_report

        # high warning -- near high fail threshold
        evaluation = evaluate_value("measurement", 24, low_fail, low_warning, high_warning, high_fail)
        assert evaluation.success
        expected_report = "WARNING: The measurement is somewhat larger than expected: 24\n"
        expected_report += "         The measurement upper bound is: 25\n"
        assert evaluation.report == expected_report

        # high fail -- on threshold
        evaluation = evaluate_value("measurement", 25, low_fail, low_warning, high_warning, high_fail)
        assert not evaluation.success
        expected_report = "FAIL: The measurement is larger than expected: 25\n"
        expected_report += "      The measurement upper bound is: 25\n"
        assert evaluation.report == expected_report

        # high fail -- typical
        evaluation = evaluate_value("measurement", 30, low_fail, low_warning, high_warning, high_fail)
        assert not evaluation.success
        expected_report = "FAIL: The measurement is larger than expected: 30\n"
        expected_report += "      The measurement upper bound is: 25\n"
        assert evaluation.report == expected_report
