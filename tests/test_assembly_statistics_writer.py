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

        # num_contigs, minimum_contig_length, n50, n75, l50, l75, gc_content, length
        qualities = [AssemblyQuality(10, 1000, 9000, 5000, 5, 3, 0.51, 25000),
                     AssemblyQuality(20, 1000, 18000, 10000, 10, 6, 0.52, 50000)]

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

        mimimum_contig_length = 1000
        writer = AssemblyStatisticsWriter(output_directory)

        platform = Platform.ILLUMINA
        species = Species("Listeria monocytogenes", 1.0)
        reads = Reads("forward.fastq", "reverse.fastq")

        # assembly database
        assembly_database = AssemblyDatabase(TEST_DATABASE_PATH)

        # num_contigs, n50, n75, l50, l75, gc_content, length
        assembly_quality = AssemblyQuality(10, mimimum_contig_length, 9000, 5000, 5, 3, 0.51, 25000)

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

        species_evaluation = AssemblyEvaluation(success, True,
                                                n50_evaluation, contigs_evaluation, l50_evaluation, length_evaluation,
                                                report)

        ncbi_evaluation = AssemblyEvaluation(success, True,
                                             n50_evaluation, contigs_evaluation, l50_evaluation, length_evaluation,
                                             report)

        machine_learning_evaluation = MachineLearningEvaluation(
            True,
            True,
            1.0,
            "The probability of the assembly being good is: 1.0"
        )

        json_file_location = writer.write_json(platform, species, reads, read_quality, assembly_quality,
                                               species_evaluation, machine_learning_evaluation, ncbi_evaluation,
                                               assembly_database)

        with open(json_file_location) as json_file:
            data = json.load(json_file)

            assert (data["technology"] == "Illumina")
            assert (data["species"] == "Listeria monocytogenes")

            assert (data["readQuality"]["totalReads"] == 1000)
            assert (data["readQuality"]["totalBases"] == 30000)
            assert (data["readQuality"]["q20Bases"] == 20000)
            assert (data["readQuality"]["q20Rate"] == pytest.approx(0.67, 0.1))
            assert (data["readQuality"]["q30Bases"] == 5000)
            assert (data["readQuality"]["q30Rate"] == pytest.approx(0.17, 0.1))
            assert (data["readQuality"]["gcContent"] == pytest.approx(0.55, 0.1))

            assert (data["assemblyQuality"]["n50"] == 9000)
            assert (data["assemblyQuality"]["l50"] == 5)
            assert (data["assemblyQuality"]["numContigs"] == 10)
            assert (data["assemblyQuality"]["minContigLength"] == mimimum_contig_length)
            assert (data["assemblyQuality"]["assemblySize"] == 25000)

            assert (data['heuristicEvaluation']['thresholds']["n50LowError"] == 142261.85)
            assert (data['heuristicEvaluation']['thresholds']["n50LowWarning"] == 297362.8)
            assert (data['heuristicEvaluation']['thresholds']["n50HighWarning"] == 546172.8)
            assert (data['heuristicEvaluation']['thresholds']["n50HighError"] == 1461919.65)

            assert (data['heuristicEvaluation']['thresholds']["l50LowError"] == 1)
            assert (data['heuristicEvaluation']['thresholds']["l50LowWarning"] == 2)
            assert (data['heuristicEvaluation']['thresholds']["l50HighWarning"] == 4)
            assert (data['heuristicEvaluation']['thresholds']["l50HighError"] == 7)

            assert (data['heuristicEvaluation']['thresholds']["contigsLowError"] == 10)
            assert (data['heuristicEvaluation']['thresholds']["contigsLowWarning"] == 14)
            assert (data['heuristicEvaluation']['thresholds']["contigsHighWarning"] == 36)
            assert (data['heuristicEvaluation']['thresholds']["contigsHighError"] == 83)

            assert (data['heuristicEvaluation']['thresholds']["lengthLowError"] == 2861443.65)
            assert (data['heuristicEvaluation']['thresholds']["lengthLowWarning"] == 2904912)
            assert (data['heuristicEvaluation']['thresholds']["lengthHighWarning"] == 3051700)
            assert (data['heuristicEvaluation']['thresholds']["lengthHighError"] == 3111649.8)

            assert not (data["heuristicEvaluation"]["success"])
            assert (data["heuristicEvaluation"]["n50Pass"])
            assert (data["heuristicEvaluation"]["contigsPass"])
            assert not (data["heuristicEvaluation"]["l50Pass"])
            assert not (data["heuristicEvaluation"]["lengthPass"])

            assert (data["machineLearningEvaluation"]["success"])
            assert (data["machineLearningEvaluation"]["probability"] == 1.0)
            assert (data["machineLearningEvaluation"]["report"] ==
                    "The probability of the assembly being good is: 1.0")
