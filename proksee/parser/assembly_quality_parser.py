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

from proksee.assembly_quality import AssemblyQuality


def parse_assembly_quality_from_quast_report(quast_filename):
    """
    Parses a QUAST TSV-format report file and creates an AssemblyQuality object from that information.

    PARAMETERS:

        quast_filename (str): the filename of the QUAST TSV-format file

    RETURNS:

        assembly_quality (AssemblyQuality): an AssemblyQuality object summarizing the information in the QUAST
        TSV-format file.
    """

    NUM_CONTIGS = "# contigs"
    N50 = "N50"
    N75 = "N75"
    L50 = "L50"
    L75 = "L75"
    GC_CONTENT = "GC (%)"

    report = {}

    if not os.path.exists(quast_filename):
        raise FileNotFoundError("File not found: " + quast_filename)

    with open(quast_filename) as file:
        for line in file:
            tokens = line.split("\t")
            key = tokens[0]
            value = tokens[1]

            report[key] = value

    num_contigs = int(report[NUM_CONTIGS])
    n50 = int(report[N50])
    n75 = int(report[N75])
    l50 = int(report[L50])
    l75 = int(report[L75])
    gc_content = float(report[GC_CONTENT])

    assembly_quality = AssemblyQuality(num_contigs, n50, n75, l50, l75, gc_content)

    return assembly_quality
