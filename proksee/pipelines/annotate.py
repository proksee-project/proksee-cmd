"""
Copyright Government of Canada 2021

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

from proksee import utilities


def annotate(contigs_filename, output_directory, resource_specification):
    """
    The main control flow of the program that evaluates the assembly.

    ARGUMENTS:
        contigs_filename (string): the filename of the contigs to evaluate
        output_directory (string): the location to place all program output and temporary files
        resource_specification (ResourceSpecification): the resources that sub-programs should use

    POST:
        The contigs with passed filename will be evaluated and the results will be written to standard output.
    """

    print(utilities.build_version_message())
