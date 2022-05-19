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

import json

from proksee.reads.read_quality import ReadQuality


def parse_read_quality_from_fastp(fastp_file):
    """
    Parses a FASTP JSON file and creates a ReadQuality object from that information.

    PARAMETERS:

        fastp_file (str): the file location of the FASTP JSON file

    RETURNS:

        read_quality (ReadQuality): a ReadQuality object summarizing the information in the FASTP JSON file.
    """

    SUMMARY = "summary"
    AFTER = "after_filtering"

    TOTAL_READS = "total_reads"
    TOTAL_BASES = "total_bases"
    Q20_BASES = "q20_bases"
    Q30_BASES = "q30_bases"
    READ1_MEDIAN_LENGTH = "read1_mean_length"
    READ2_MEDIAN_LENGTH = "read2_mean_length"
    GC_CONTENT = "gc_content"

    with open(fastp_file) as file:
        data = json.load(file)

    summary = data[SUMMARY]  # Summary information about the quality.
    after = summary[AFTER]  # Quality of the reads, after filtering.

    total_reads = after[TOTAL_READS]
    total_bases = after[TOTAL_BASES]
    q20_bases = after[Q20_BASES]
    q30_bases = after[Q30_BASES]
    forward_median_length = after[READ1_MEDIAN_LENGTH]
    reverse_median_length = after[READ2_MEDIAN_LENGTH] if READ2_MEDIAN_LENGTH in after else 0
    gc_content = after[GC_CONTENT]

    read_quality = ReadQuality(total_reads, total_bases, q20_bases, q30_bases, forward_median_length,
                               reverse_median_length, gc_content)

    return read_quality
