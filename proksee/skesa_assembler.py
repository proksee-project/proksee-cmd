"""
Copyright Government of Canada 2020

Written by:

Arnab Saha Mandal
    University of Manitoba
    National Microbiology Laboratory, Public Health Agency of Canada

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
import subprocess
import sys

from proksee.assembler import Assembler


class SkesaAssembler(Assembler):
    """
    A class representing a Skesa assembler.

    ATTRIBUTES
        contigs_filename (str): the filename of the assembled contigs output
    """

    DIRECTORY_NAME = "skesa"

    def __init__(self, reads, output_dir, resource_specification):
        """
        Initializes the Skesa assembler.

        PARAMETERS
            reads (Reads): the reads to assemble
            output_dir (str): the filename of the output directory
            resource_specification (ResourceSpecification): the resources that the assembler should use
        """

        NAME = "Skesa"

        skesa_directory = os.path.join(output_dir, self.DIRECTORY_NAME)
        super().__init__(NAME, reads, skesa_directory, resource_specification)

        self.contigs_filename = os.path.join(skesa_directory, 'contigs.fasta')
        self.log_filename = os.path.join(skesa_directory, 'skesa.log')

    def build_command(self):
        """
        Builds the command line string for running Skesa.

        RETURNS
            command (str): the command for running Skesa on the command line
        """

        # (below we assumes cores = threads)

        if self.reads.reverse is None:
            command = "skesa --fastq " + self.reads.forward + \
                      " --cores " + str(self.resource_specification.threads) + \
                      " --memory " + str(self.resource_specification.memory)

        else:
            command = "skesa --fastq " + self.reads.forward + \
                      "," + self.reads.reverse + \
                      " --cores " + str(self.resource_specification.threads) + \
                      " --memory " + str(self.resource_specification.memory)

        return command

    def run_skesa(self):
        """
        Runs the Skesa assembler on the reads.

        POST
            The assembled reads will be written into the output directory.
        """

        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

        output = open(self.contigs_filename, 'w+')
        logfile = open(self.log_filename, 'w+')

        command = self.build_command()

        try:
            subprocess.check_call(command, shell=True, stdout=output, stderr=logfile)

        except subprocess.CalledProcessError:
            message = "ERROR: Encountered an error when performing a SKESA assembly.\n" \
                + "       Please see the log file for more information: " + str(self.log_filename) + "\n"

            print(message)
            sys.exit(1)

        finally:
            output.close()
            logfile.close()

    def assemble(self):
        """
        Assembles the reads.

        RETURNS
            output (str): an output string reporting the result back to the user

        POST
            If completed without error, the output will be placed in the output directory.
        """

        self.run_skesa()
        output_string = "Assembled reads using Skesa."

        return output_string

    def get_contigs_filename(self):
        """
        Gets the filename of the assembled contigs.

        RETURNS
            filename (str): the filename of the assembled contigs
        """

        return self.contigs_filename
