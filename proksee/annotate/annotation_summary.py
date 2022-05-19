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


class AnnotationSummary:
    """
    A class containing a variety annotation summary metrics.

    ATTRIBUTES:

            organism (str): the name of the organism
            contigs (int): the number of contigs
            bases (int): the number of bases
            cds (int): the number of CDS regions
            rRNA (int): the number of rRNA elements
            tRNA (int): the number of tRNA elements
    """

    def __init__(self, organism, contigs, bases, cds, rRNA, tRNA):
        """
        PARAMETERS:

            organism (str): the name of the organism
            contigs (int): the number of contigs
            bases (int): the number of bases
            cds (int): the number of CDS regions
            rRNA (int): the number of rRNA elements
            tRNA (int): the number of tRNA elements
        """

        self.organism = organism
        self.contigs = contigs
        self.bases = bases
        self.cds = cds
        self.rRNA = rRNA
        self.tRNA = tRNA

    def generate_report(self):
        """
        Generates a multi-line text report.

        RETURNS:
            summary (str): a multi-line text report for the summary
        """

        summary = ""

        summary += "organism: " + str(self.organism) + "\n"
        summary += "contigs: " + str(self.contigs) + "\n"
        summary += "bases: " + str(self.bases) + "\n"
        summary += "cds: " + str(self.cds) + "\n"
        summary += "rRNA: " + str(self.rRNA) + "\n"
        summary += "tRNA: " + str(self.tRNA) + "\n"

        return summary
