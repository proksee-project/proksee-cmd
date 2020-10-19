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


class AssemblyQuality:
    """
    A class representing the quality of an assembly.
    ATTRIBUTES:
            num_contigs (int): the number of contigs in the assembly
            n50 (int): shortest contig needed to cover 50% of the assembly
            n75 (int): shortest contig needed to cover 75% of the assembly
            l50 (int): the length of the shortest contig needed to cover 50% of the assembly
            l75 (int): the length of the shortest contig needed to cover 75% of the assembly
            gc_content (float): the GC-ratio of the bases in the assembly
    """

    def __init__(self, num_contigs, n50, n75, l50, l75, gc_content):
        """
        Initializes the AssemblyQuality object.
        PARAMETERS:
            num_contigs (int): the number of contigs in the assembly
            n50 (int): shortest contig needed to cover 50% of the assembly
            n75 (int): shortest contig needed to cover 75% of the assembly
            l50 (int): the length of the shortest contig needed to cover 50% of the assembly
            l75 (int): the length of the shortest contig needed to cover 75% of the assembly
            gc_content (float): the GC-ratio of the bases in the assembly
        """

        self.num_contigs = num_contigs

        self.n50 = n50
        self.n75 = n75

        self.l50 = l50
        self.l75 = l75

        self.gc_content = gc_content
