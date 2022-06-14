"""
Copyright Government of Canada 2022

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

from proksee.annotator import Annotator


class ProkkaAnnotator(Annotator):
    """
    A class representing a Prokka annotator.

    ATTRIBUTES
        output_filename (str): the filename Prokka standard output
        prokka_output_directory (str): the directory of Prokka's output (specifically, not Proksee's Prokka directory)
    """

    DIRECTORY_NAME = "prokka"

    def __init__(self, contigs_filepath, output_directory, resource_specification):
        """
        Initializes the Prokka annotator.

        PARAMETERS
            contigs_filepath (str): the filepath of the contigs to annotate
            output_directory (str): the filepath of the output directory
            resource_specification (ResourceSpecification): the resources that the annotator should use
        """

        NAME = "Prokka"

        # The output directory (prokka/output) needs to exist, because we need an output directory (prokka)
        # but the Prokka program expects the output directory to not exist at runtime.
        # That's why we need an additional "output" level for the Prokka output.
        # "output_directory" = "prokka" -> Proksee output directory
        # "prokka_output_directory" = "prokka/output" -> Prokka output directory

        prokka_directory = os.path.join(output_directory, self.DIRECTORY_NAME)
        self.prokka_output_directory = os.path.join(prokka_directory, "output")
        super().__init__(NAME, contigs_filepath, prokka_directory, resource_specification)

        self.output_filename = os.path.join(self.output_directory, 'prokka.out')
        self.log_filename = os.path.join(prokka_directory, 'prokka.log')

    def build_command(self):
        """
        Builds the command line string for running Prokka.

        RETURNS
            command (str): the command for running Prokka on the command line
        """

        # (below we assumes cpus = threads)

        command = "prokka " + self.contigs_filepath + \
                  " --outdir " + self.prokka_output_directory + \
                  " --prefix prokka " + \
                  " --cpus " + str(self.resource_specification.threads)

        return command

    def annotate(self):
        """
        Annotates the contigs.

        RETURNS
            output (str): an output string reporting the result back to the user

        POST
            If completed without error, the output will be placed in the output directory.
        """

        if not os.path.isdir(self.output_directory):
            os.mkdir(self.output_directory)

        output = open(self.output_filename, 'w+')  # Console output
        logfile = open(self.log_filename, 'w+')

        command = self.build_command()

        try:
            subprocess.check_call(command, shell=True, stdout=output, stderr=logfile)

        except subprocess.CalledProcessError:
            message = "ERROR: Encountered an error when performing a Prokka annotation.\n" \
                + "       Please see the log file for more information: " + str(self.log_filename) + "\n"

            print(message)
            sys.exit(1)

        finally:
            output.close()
            logfile.close()

        message = "Annotations complete and located in " + str(self.prokka_output_directory) + "."

        return message

    def get_summary_filename(self):
        """
        Gets the filename of the annotation summary.

        RETURNS
            filename (str): the filename of the summary
        """

        # TODO: Update to correct output file
        return os.path.join(self.prokka_output_directory, "prokka.txt")
