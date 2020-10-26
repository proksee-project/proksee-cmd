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


class ReadQuality:
    """
    A class containing a variety of read quality metrics.

    ATTRIBUTES:

            total_reads (int): the total number of reads
            total_bases (int): the total number of bases in all reads
            q20_bases (int): the number of bases with quality 20 or greater
            q30_bases (int): the number of bases with quality 30 or greater
            q20_rate (float): the rate of bases with quality 20 or greater
            q30_rate (float): the rate of bases with quality 30 or greater
            forward_median_length (float): median length of the forward reads
            reverse_median_length (float): median length of the reverse reads
            gc_content (float): the GC-ratio of the bases in all reads
    """

    def __init__(self, total_reads, total_bases, q20_bases, q30_bases, forward_median_length, reverse_median_length,
                 gc_content):
        """
        Initializes the ReadQuality object.

        PARAMETERS:

            total_reads (int): the total number of reads
            total_bases (int): the total number of bases in all reads
            q20_bases (int): the number of bases with quality 20 or greater
            q30_bases (int): the number of bases with quality 30 or greater
            forward_median_length (float): median length of the forward reads
            reverse_median_length (float): median length of the reverse reads
            gc_content (float): the GC-ratio of the bases in all reads
        """

        self.total_reads = total_reads
        self.total_bases = total_bases
        self.q20_bases = q20_bases
        self.q30_bases = q30_bases

        self.q20_rate = q20_bases / total_bases
        self.q30_rate = q30_bases / total_bases

        self.forward_median_length = forward_median_length
        self.reverse_median_length = reverse_median_length

        self.gc_content = gc_content
