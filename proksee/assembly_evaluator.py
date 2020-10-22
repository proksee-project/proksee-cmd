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
