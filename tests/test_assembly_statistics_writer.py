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

import os
import csv

from proksee.assembly_quality import AssemblyQuality
from proksee.writer.assembly_statistics_writer import AssemblyStatisticsWriter


class TestAssemblyStatisticsWriter:

    def test_simple_statistics(self):
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

        # Remove existing test file if it exists:
        if os.path.isfile(writer.output_filename):
            os.remove(writer.output_filename)

        writer.write(names, qualities)

        with open(writer.output_filename) as csvfile:

            csv_reader = csv.reader(csvfile, delimiter=',')

            row = next(csv_reader)
            assert row == ["", "Number of Contigs", "N50", "L50", "GC Content", "Length"]

            row = next(csv_reader)
            assert row == ["test1", "10", "9000", "5", "0.51", "25000"]

            row = next(csv_reader)
            assert row == ["test2", "20", "18000", "10", "0.52", "50000"]
