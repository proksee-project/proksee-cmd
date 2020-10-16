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

from proksee.read_quality import ReadQuality


# FASTP JSON has a lot of information we might want to use
def parse_read_quality_from_fastp(fastp_file):
    print("Parsing...")

    with open(fastp_file) as file:
        data = json.load(file)

    summary = data["summary"]
    after = summary["after_filtering"]

    total_reads = after["total_reads"]
    total_bases = after["total_bases"]
    q20_bases = after["q20_bases"]
    q30_bases = after["q30_bases"]
    forward_median_length = after["read1_mean_length"]
    reverse_median_length = after["read2_mean_length"] if "read2_mean_length" in after else 0
    gc_content = after["gc_content"]

    read_quality = ReadQuality(total_reads, total_bases, q20_bases, q30_bases, forward_median_length,
                               reverse_median_length, gc_content)

    return read_quality
