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

from proksee.assembler import Assembler


class SpadesAssembler(Assembler):
    """
    A class representing a SPAdes assembler.
    """

    def __init__(self, forward, reverse, output_dir):
        super().__init__(forward, reverse, output_dir)

    def run_spades(self):
        """
        Runs the SPAdes assembler on the reads.

        POST
            The assembled reads will be written into the output directory.
        """

        output_filename = os.path.join(self.output_dir, 'spades.o')
        output = open(output_filename, 'w+')

        error_filename = os.path.join(self.output_dir, 'spades.e')
        error = open(error_filename, 'w+')

        if self.reverse is None:
            command = "spades.py -s " + str(self.forward) + " -o " + str(self.output_dir)
        else:
            command = "spades.py -1 " + str(self.forward) + " -2 " + str(self.reverse) + " -o " + str(self.output_dir)

        try:
            subprocess.check_call(command, shell=True, stdout=output, stderr=error)

        except subprocess.CalledProcessError as exception:
            raise exception

        finally:
            output.close()
            error.close()

    def assemble(self):
        """
        Assembles the reads.

        RETURNS
            output (str): an output string reporting the result back to the user

        POST
            If completed without error, the reads will be assembled and output will be written to the output directory.
        """

        self.run_spades()

        output = "Assembled reads using SPAdes."
        return output
