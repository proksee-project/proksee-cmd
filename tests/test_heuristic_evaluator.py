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
from pathlib import Path

from proksee.assembly_database import AssemblyDatabase
from proksee.assembly_quality import AssemblyQuality
from proksee.heuristic_evaluator import evaluate_value, compare_assemblies, HeuristicEvaluator
from proksee.species import Species


class TestHeuristicEvaluator:

    def test_evaluate_value(self):
        """
        Tests the ability to evaluate whether a value is high or low.
        """

        low_fail = 5
        low_warning = 10
        high_warning = 20
        high_fail = 25

        # fail -- too low
        evaluation = evaluate_value("measurement", 2, low_warning, high_warning, low_fail, high_fail)
        assert not evaluation.success
        expected_report = "FAIL: The measurement is smaller than expected: 2\n"
        expected_report += "      The measurement lower bound is: 5\n"
        assert evaluation.report == expected_report

        # fail (but warning) -- too low, low failure disabled
        evaluation = evaluate_value("measurement", 2, low_warning, high_warning, low_fail=None, high_fail=high_fail)
        assert evaluation.success
        expected_report = "WARNING: The measurement is smaller than expected: 2\n"
        expected_report += "         The measurement lower warning bound is: 10\n"
        assert evaluation.report == expected_report

        # fail -- too low, on threshold
        evaluation = evaluate_value("measurement", 5, low_warning, high_warning, low_fail, high_fail)
        assert not evaluation.success
        expected_report = "FAIL: The measurement is smaller than expected: 5\n"
        expected_report += "      The measurement lower bound is: 5\n"
        assert evaluation.report == expected_report

        # low warning -- above low fail threshold
        evaluation = evaluate_value("measurement", 6, low_warning, high_warning, low_fail, high_fail)
        assert evaluation.success
        expected_report = "WARNING: The measurement is smaller than expected: 6\n"
        expected_report += "         The measurement lower warning bound is: 10\n"
        assert evaluation.report == expected_report

        # low warning -- on low warning threshold
        evaluation = evaluate_value("measurement", 10, low_warning, high_warning, low_fail, high_fail)
        assert evaluation.success
        expected_report = "WARNING: The measurement is smaller than expected: 10\n"
        expected_report += "         The measurement lower warning bound is: 10\n"
        assert evaluation.report == expected_report

        # acceptable -- above low warning threshold
        evaluation = evaluate_value("measurement", 11, low_warning, high_warning, low_fail, high_fail)
        assert evaluation.success
        expected_report = "PASS: The measurement is comparable to similar assemblies: 11\n"
        expected_report += "      The preferred measurement range is: (10, 20)\n"
        assert evaluation.report == expected_report

        # acceptable -- typical
        evaluation = evaluate_value("measurement", 15, low_warning, high_warning, low_fail, high_fail)
        assert evaluation.success
        expected_report = "PASS: The measurement is comparable to similar assemblies: 15\n"
        expected_report += "      The preferred measurement range is: (10, 20)\n"
        assert evaluation.report == expected_report

        # acceptable -- below high warning threshold
        evaluation = evaluate_value("measurement", 19, low_warning, high_warning, low_fail, high_fail)
        assert evaluation.success
        expected_report = "PASS: The measurement is comparable to similar assemblies: 19\n"
        expected_report += "      The preferred measurement range is: (10, 20)\n"
        assert evaluation.report == expected_report

        # high warning -- on threshold
        evaluation = evaluate_value("measurement", 20, low_warning, high_warning, low_fail, high_fail)
        assert evaluation.success
        expected_report = "WARNING: The measurement is larger than expected: 20\n"
        expected_report += "         The measurement upper warning bound is: 20\n"
        assert evaluation.report == expected_report

        # high warning -- near high fail threshold
        evaluation = evaluate_value("measurement", 24, low_warning, high_warning, low_fail, high_fail)
        assert evaluation.success
        expected_report = "WARNING: The measurement is larger than expected: 24\n"
        expected_report += "         The measurement upper warning bound is: 20\n"
        assert evaluation.report == expected_report

        # high fail -- on threshold
        evaluation = evaluate_value("measurement", 25, low_warning, high_warning, low_fail, high_fail)
        assert not evaluation.success
        expected_report = "FAIL: The measurement is larger than expected: 25\n"
        expected_report += "      The measurement upper bound is: 25\n"
        assert evaluation.report == expected_report

        # high fail -- typical
        evaluation = evaluate_value("measurement", 30, low_warning, high_warning, low_fail, high_fail)
        assert not evaluation.success
        expected_report = "FAIL: The measurement is larger than expected: 30\n"
        expected_report += "      The measurement upper bound is: 25\n"
        assert evaluation.report == expected_report

        # high fail (warning) -- high failure, but high failure disabled
        evaluation = evaluate_value("measurement", 30, low_warning, high_warning, low_fail=low_fail, high_fail=None)
        assert evaluation.success
        expected_report = "WARNING: The measurement is larger than expected: 30\n"
        expected_report += "         The measurement upper warning bound is: 20\n"
        assert evaluation.report == expected_report

    def test_compare_assemblies(self):
        """
        Tests comparison of two assemblies.
        """

        # num_contigs, n50, n75, l50, l75, gc_content, length
        qualities = [AssemblyQuality(10, 9000, 5000, 5, 3, 0.51, 25000),
                     AssemblyQuality(20, 18000, 10000, 10, 6, 0.52, 50000)]

        report = compare_assemblies(qualities[0], qualities[1])

        expected = "Changes in assembly statistics:\n"
        expected += "N50: 9000\n"
        expected += "Number of Contigs: 10\n"
        expected += "L50: 5\n"
        expected += "Length: 25000\n"
        expected += "\n"

        assert report == expected

    def test_evaluate_assembly_from_fallback(self):
        """
        Tests the fallback heuristic evaluation (when the species is not present in the assembly database).
        """

        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database",
                                     "refseq_short.csv")
        species = Species("not a species", 1.0)

        database = AssemblyDatabase(DATABASE_PATH)
        evaluator = HeuristicEvaluator(species, database)  # Need to instantiate child class.

        # Good assembly
        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(1000, 6000, 5500, 300, 350, 0.50, 2475580)
        evaluation = evaluator.evaluate(assembly_quality)
        assert evaluation.success

        # Too many contigs
        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(10000, 6000, 5500, 300, 350, 0.50, 2475580)
        evaluation = evaluator.evaluate(assembly_quality)
        assert not evaluation.success
        assert evaluation.n50_evaluation.success
        assert evaluation.l50_evaluation.success
        assert not evaluation.contigs_evaluation.success
        assert evaluation.length_evaluation.success

        # N50 too small
        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(1000, 1000, 500, 300, 350, 0.50, 2475580)
        evaluation = evaluator.evaluate(assembly_quality)
        assert not evaluation.success
        assert not evaluation.n50_evaluation.success
        assert evaluation.l50_evaluation.success
        assert evaluation.contigs_evaluation.success
        assert evaluation.length_evaluation.success

        # L50 too large
        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(1000, 6000, 5500, 1000, 2000, 0.50, 2475580)
        evaluation = evaluator.evaluate(assembly_quality)
        assert not evaluation.success
        assert evaluation.n50_evaluation.success
        assert not evaluation.l50_evaluation.success
        assert evaluation.contigs_evaluation.success
        assert evaluation.length_evaluation.success

        # length too small
        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(1000, 6000, 5500, 300, 350, 0.50, 100)
        evaluation = evaluator.evaluate(assembly_quality)
        assert not evaluation.success
        assert evaluation.n50_evaluation.success
        assert evaluation.l50_evaluation.success
        assert evaluation.contigs_evaluation.success
        assert not evaluation.length_evaluation.success
