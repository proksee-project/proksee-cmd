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

from proksee.prokka_annotator import ProkkaAnnotator
from proksee.parser.prokka_parser import parse_prokka_summary_from_txt


def annotate(contigs_filename, output_directory, resource_specification):
    """
    Performs and evaluates sequence annotation.

    ARGUMENTS:
        contigs_filename (string): the filename of the contigs to evaluate
        output_directory (string): the location to place all program output and temporary files
        resource_specification (ResourceSpecification): the resources that sub-programs should use

    POST:
        The contigs with passed filename will be annotated and evaluated. The results will be written to standard
        output.
    """

    # Make output directory:
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    print("Annotating with Prokka!\n")

    prokka_annotator = ProkkaAnnotator(contigs_filename, output_directory, resource_specification)
    output = prokka_annotator.annotate()
    print(output + "\n")

    prokka_text_summary_filename = prokka_annotator.get_summary_filename()
    prokka_summary = parse_prokka_summary_from_txt(prokka_text_summary_filename)

    print(prokka_summary.generate_report())
    print("Complete!")
