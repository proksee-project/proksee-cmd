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


def parse_assembly_quality_from_quast_report(quast_filename, minimum_contig_length):
    """
    Parses a QUAST TSV-format report file and creates an AssemblyQuality object from that information.

    PARAMETERS:

        quast_filename (str): the filename of the QUAST TSV-format file
        minimum_contig_length (int): the minimum contig length; this is necessary because the number is
            used to parse the output of the QUAST report

    RETURNS:

        assembly_quality (AssemblyQuality): an AssemblyQuality object summarizing the information in the QUAST
        TSV-format file.
    """

    NUM_CONTIGS_UNFILTERED = "# contigs (>= 0 bp)"
    NUM_CONTIGS_FILTERED = "# contigs (>= " + str(minimum_contig_length) + " bp)"
    N50 = "N50"
    N75 = "N75"
    L50 = "L50"
    L75 = "L75"
    GC_CONTENT = "GC (%)"
    TOTAL_LENGTH_UNFILTERED = "Total length (>= 0 bp)"
    TOTAL_LENGTH_FILTERED = "Total length (>= " + str(minimum_contig_length) + " bp)"

    report = {}

    if not os.path.exists(quast_filename):
        raise FileNotFoundError("File not found: " + quast_filename)

    with open(quast_filename) as file:
        for line in file:
            tokens = line.split("\t")
            key = tokens[0]
            value = tokens[1]

            report[key] = value

    num_contigs_unfiltered = int(report[NUM_CONTIGS_UNFILTERED])
    num_contigs_filtered = int(report[NUM_CONTIGS_FILTERED])
    n50 = int(report[N50])
    n75 = int(report[N75])
    l50 = int(report[L50])
    l75 = int(report[L75])
    gc_content = float(report[GC_CONTENT]) / 100.0  # Quast reports as a percentage
    total_length_unfiltered = int(report[TOTAL_LENGTH_UNFILTERED])
    total_length_filtered = int(report[TOTAL_LENGTH_FILTERED])

    assembly_quality = AssemblyQuality(num_contigs_unfiltered, num_contigs_filtered, minimum_contig_length,
                                       n50, n75, l50, l75, gc_content, total_length_unfiltered, total_length_filtered)

    return assembly_quality
