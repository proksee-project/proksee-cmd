"""
Copyright Government of Canada 2022

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

from proksee.annotate.annotation_summary import AnnotationSummary


def parse_prokka_summary_from_txt(prokka_text_file):
    """
    Parses a Prokka text output summary file and creates a AnnotationSummary object from that information.

    The Prokka text output file is expected to start with the following format:

    organism: [STRING]
    contigs: [INT]
    bases: [INT]

    Then, the output file may optionally have the following lines:

    CDS: [INT]
    rRNA: [INT]
    tRNA: [INT]

    PARAMETERS:
        prokka_text_file (str): the file location of the Prokka text output file

    RETURNS:
        annotation_summary (AnnotationSummary): an object encapsulating the information in the Prokka text file
    """

    DELIMETER = ": "

    ORGANISM = "organism"
    CONTIGS = "contigs"
    BASES = "bases"
    CDS = "CDS"
    RRNA = "rRNA"
    TRNA = "tRNA"

    # Initialize, because there may be missing values.
    organism = "Unknown"
    contigs = 0
    bases = 0
    cds = 0
    rRNA = 0
    tRNA = 0

    with open(prokka_text_file) as file:

        for line in file:
            tokens = line.split(DELIMETER)
            key = tokens[0]
            value = tokens[1].strip()

            if key == ORGANISM:
                organism = str(value)
            elif key == CONTIGS:
                contigs = int(value)
            elif key == BASES:
                bases = int(value)
            elif key == CDS:
                cds = int(value)
            elif key == RRNA:
                rRNA = int(value)
            elif key == TRNA:
                tRNA = int(value)

    annotation_summary = AnnotationSummary(organism, contigs, bases, cds, rRNA, tRNA)

    return annotation_summary
