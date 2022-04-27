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
import subprocess
import sys

from proksee.assembler import Assembler


class SpadesAssembler(Assembler):
    """
    A class representing a SPAdes assembler.

    ATTRIBUTES
        contigs_filename (str): the filename of the assembled contigs output
    """

    DIRECTORY_NAME = "spades"

    def __init__(self, reads, output_dir, resource_specification):
        """
        Initializes the SPAdes assembler.

        PARAMETERS
            reads (Reads): the reads to assemble
            output_dir (str): the filename of the output directory
            resource_specification (ResourceSpecification): the specification of resource that the assembler should use
        """

        NAME = "SPAdes"

        spades_directory = os.path.join(output_dir, self.DIRECTORY_NAME)
        super().__init__(NAME, reads, spades_directory, resource_specification)

        self.contigs_filename = os.path.join(spades_directory, "contigs.fasta")

    def run_spades(self):
        """
        Runs the SPAdes assembler on the reads.

        POST
            The assembled reads will be written into the output directory.
        """

        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

        output_filename = os.path.join(self.output_dir, 'spades.o')
        output = open(output_filename, 'w+')

        error_filename = os.path.join(self.output_dir, 'spades.e')
        error = open(error_filename, 'w+')

        if self.reads.reverse is None:
            command = "spades.py -s " + str(self.reads.forward) + \
                      " -o " + str(self.output_dir) + \
                      " -t " + str(self.resource_specification.threads) + \
                      " -m " + str(self.resource_specification.memory)
        else:
            command = "spades.py -1 " + str(self.reads.forward) + \
                      " -2 " + str(self.reads.reverse) + \
                      " -o " + str(self.output_dir) + \
                      " -t " + str(self.resource_specification.threads) + \
                      " -m " + str(self.resource_specification.memory)

        try:
            subprocess.check_call(command, shell=True, stdout=output, stderr=error)

        except subprocess.CalledProcessError:

            message = "ERROR: Encountered an error when performing a SPAdes assembly.\n" \
                + "       Please see the error file for more information: " + str(error_filename) + "\n"

            print(message)
            sys.exit(1)

        finally:
            output.close()
            error.close()

    def assemble(self):
        """
        Assembles the reads.

        RETURNS
            output (str): an output string reporting the result back to the user

        POST
            If completed without error, the output will be placed in the output directory.
        """

        self.run_spades()

        output = "Assembled reads using SPAdes."
        return output

    def get_contigs_filename(self):
        """
        Gets the filename of the assembled contigs.

        RETURNS
            filename (str): the filename of the assembled contigs
        """

        return self.contigs_filename
