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

from proksee.prokka_summary import ProkkaSummary


def parse_prokka_summary_from_txt(prokka_text_file):
    """
    Parses a Prokka text output summary file and creates a ProkkaSummary object from that information.

    The Prokka text output file is expected to have the following format:

    organism: [STRING]
    contigs: [INT]
    bases: [INT]
    CDS: [INT]
    rRNA: [INT]
    tRNA: [INT]

    PARAMETERS:
        prokka_text_file (str): the file location of the Prokka text output file

    RETURNS:
        prokka_summary (ProkkaSummary): an object encapsulating the information in the Prokka text file
    """

    with open(prokka_text_file) as file:

        line = file.readline()
        organism = str(line.split(":")[1].strip())

        line = file.readline()
        contigs = int(line.split(":")[1].strip())

        line = file.readline()
        bases = int(line.split(":")[1].strip())

        line = file.readline()
        cds = int(line.split(":")[1].strip())

        line = file.readline()
        rRNA = int(line.split(":")[1].strip())

        line = file.readline()
        tRNA = int(line.split(":")[1].strip())

    prokka_summary = ProkkaSummary(organism, contigs, bases, cds, rRNA, tRNA)

    return prokka_summary
