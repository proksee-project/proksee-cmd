"""
Copyright Government of Canada 2020

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
import json
import os
import csv
import pytest

from pathlib import Path

from proksee.assembly_quality import AssemblyQuality
from proksee.evaluation import AssemblyEvaluation, Evaluation, MachineLearningEvaluation
from proksee.platform_identify import Platform
from proksee.read_quality import ReadQuality
from proksee.reads import Reads
from proksee.species import Species
from proksee.writer.assembly_statistics_writer import AssemblyStatisticsWriter
from proksee.assembly_database import AssemblyDatabase

TEST_DATABASE_PATH = os.path.join(Path(__file__).parent.absolute(), "data", "test_database.csv")


class TestAssemblyStatisticsWriter:

    def test_write_simple_statistics_csv(self):
        """
        Tests writing valid and simple assembly statistics.
        """

        output_directory = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "temp")

        writer = AssemblyStatisticsWriter(output_directory)
        names = ["test1", "test2"]

        # num_contigs, n50, n75, l50, l75, gc_content, length
        qualities = [AssemblyQuality(10, 9000, 5000, 5, 3, 0.51, 25000),
                     AssemblyQuality(20, 18000, 10000, 10, 6, 0.52, 50000)]

        csv_filename = writer.write_csv(names, qualities)

        with open(csv_filename) as csvfile:

            csv_reader = csv.reader(csvfile, delimiter=',')

            row = next(csv_reader)
            assert row == ["Assembly Name", "Number of Contigs", "N50", "L50", "GC Content", "Length"]

            row = next(csv_reader)
            assert row == ["test1", "10", "9000", "5", "0.51", "25000"]

            row = next(csv_reader)
            assert row == ["test2", "20", "18000", "10", "0.52", "50000"]

    def test_json_writer_valid(self):
        """
        Tests JSON file writing when the data is simple and valid.
        """

        output_directory = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "data", "temp")

        writer = AssemblyStatisticsWriter(output_directory)

        platform = Platform.ILLUMINA
        species = Species("Listeria monocytogenes", 1.0)
        reads = Reads("forward.fastq", "reverse.fastq")

        # assembly database
        assembly_database = AssemblyDatabase(TEST_DATABASE_PATH)

        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(10, 9000, 5000, 5, 3, 0.51, 25000)

        # total_reads, total_bases, q20_bases, q30_bases, forward_median_length, reverse_median_length, gc_content
        read_quality = ReadQuality(1000, 30000, 20000, 5000, 150, 140, 0.55)

        n50_evaluation = Evaluation(True, "The N50 looks good!")
        contigs_evaluation = Evaluation(True, "The contigs look good!")
        l50_evaluation = Evaluation(False, "The L50 looks bad!")
        length_evaluation = Evaluation(False, "The length looks bad!")

        success = n50_evaluation.success and contigs_evaluation.success \
            and l50_evaluation.success and length_evaluation.success

        report = "\n"
        report += n50_evaluation.report
        report += contigs_evaluation.report
        report += l50_evaluation.report
        report += length_evaluation.report

        heuristic_evaluation = AssemblyEvaluation(n50_evaluation, contigs_evaluation, l50_evaluation, length_evaluation,
                                                  success, report)

        machine_learning_evaluation = MachineLearningEvaluation(
            True,
            "The probability of the assembly being good is: 1.0",
            1.0,
            True
        )

        json_file_location = writer.write_json(platform, species, reads, read_quality, assembly_quality,
                                               heuristic_evaluation, machine_learning_evaluation, assembly_database)

        with open(json_file_location) as json_file:
            data = json.load(json_file)

            assert (data["Technology"] == "Illumina")
            assert (data["Species"] == "Listeria monocytogenes")

            assert (data["Read Quality"]["Total Reads"] == 1000)
            assert (data["Read Quality"]["Total Bases"] == 30000)
            assert (data["Read Quality"]["Q20 Bases"] == 20000)
            assert (data["Read Quality"]["Q20 Rate"] == pytest.approx(0.67, 0.1))
            assert (data["Read Quality"]["Q30 Bases"] == 5000)
            assert (data["Read Quality"]["Q30 Rate"] == pytest.approx(0.17, 0.1))
            assert (data["Read Quality"]["GC Content"] == pytest.approx(0.55, 0.1))

            assert (data["Assembly Quality"]["N50"] == 9000)
            assert (data["Assembly Quality"]["L50"] == 5)
            assert (data["Assembly Quality"]["Number of Contigs"] == 10)
            assert (data["Assembly Quality"]["Assembly Size"] == 25000)

            assert (data["Assembly Thresholds"]["N50 Low Error"] == 142261.85)
            assert (data["Assembly Thresholds"]["N50 Low Warning"] == 297362.8)
            assert (data["Assembly Thresholds"]["N50 High Warning"] == 546172.8)
            assert (data["Assembly Thresholds"]["N50 High Error"] == 1461919.65)

            assert (data["Assembly Thresholds"]["L50 Low Error"] == 1)
            assert (data["Assembly Thresholds"]["L50 Low Warning"] == 2)
            assert (data["Assembly Thresholds"]["L50 High Warning"] == 4)
            assert (data["Assembly Thresholds"]["L50 High Error"] == 7)

            assert (data["Assembly Thresholds"]["Contigs Low Error"] == 10)
            assert (data["Assembly Thresholds"]["Contigs Low Warning"] == 14)
            assert (data["Assembly Thresholds"]["Contigs High Warning"] == 36)
            assert (data["Assembly Thresholds"]["Contigs High Error"] == 83)

            assert (data["Assembly Thresholds"]["Length Low Error"] == 2861443.65)
            assert (data["Assembly Thresholds"]["Length Low Warning"] == 2904912)
            assert (data["Assembly Thresholds"]["Length High Warning"] == 3051700)
            assert (data["Assembly Thresholds"]["Length High Error"] == 3111649.8)

            assert not (data["Heuristic Evaluation"]["Success"])
            assert (data["Heuristic Evaluation"]["N50 Pass"])
            assert (data["Heuristic Evaluation"]["N50 Report"] == "The N50 looks good!")
            assert (data["Heuristic Evaluation"]["Contigs Pass"])
            assert (data["Heuristic Evaluation"]["Contigs Report"] == "The contigs look good!")
            assert not (data["Heuristic Evaluation"]["L50 Pass"])
            assert (data["Heuristic Evaluation"]["L50 Report"] == "The L50 looks bad!")
            assert not (data["Heuristic Evaluation"]["Length Pass"])
            assert (data["Heuristic Evaluation"]["Length Report"] == "The length looks bad!")

            assert (data["Machine Learning Evaluation"]["Success"])
            assert (data["Machine Learning Evaluation"]["Probability"] == 1.0)
            assert (data["Machine Learning Evaluation"]["Report"] ==
                    "The probability of the assembly being good is: 1.0")
