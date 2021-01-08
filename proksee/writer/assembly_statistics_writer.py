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

import csv
import os


class AssemblyStatisticsWriter:
    """
    A class for writing assembly statistics to file.

    ATTRIBUTES
        output_filename (str): the location of the output file
    """

    def __init__(self, output_directory):
        """
        Initializes the assembly statistics writer.

        PARAMETERS
            output_directory (str): the location of the directory to write output files

        POST
            The output directory will be created if it is missing.
        """

        if not os.path.isdir(output_directory):
            os.mkdir(output_directory)

        self.output_filename = os.path.join(output_directory, "assembly_statistics.csv")

    def write(self, names, qualities):
        """
        Writes the assembly statistics to the output file.

        PARAMETERS
            names (List(str)): a list of names of the assemblies; should be the same length as qualities
            qualities (List(AssemblyQuality)): a list of AssemblyQuality objects; should be the same length as names

        POST
            The assembly statistics will be written to the output file.
        """

        with open(self.output_filename, "w") as csvfile:

            ASSEMBLY_NAME = "Assembly Name"
            NUM_CONTIGS = "Number of Contigs"
            N50 = "N50"
            L50 = "L50"
            GC_CONTENT = "GC Content"
            LENGTH = "Length"

            csv_writer = csv.writer(csvfile, delimiter=',')

            headers = [ASSEMBLY_NAME, NUM_CONTIGS, N50, L50, GC_CONTENT, LENGTH]
            csv_writer.writerow(headers)

            for i in range(len(names)):
                name = names[i]
                quality = qualities[i]

                row = [name, quality.num_contigs, quality.n50, quality.l50, quality.gc_content, quality.length]
                csv_writer.writerow(row)
