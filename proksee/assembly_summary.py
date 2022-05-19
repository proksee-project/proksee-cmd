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


class AssemblySummary:
    """
    A class encapsulating information about a sequence assembly.

    ATTRIBUTES:

            species (str): the name of the species
            assembly_quality (str): an object encapsulating the quality of the assembly
            contigs_filename (str): the file name of the contigs output from the assembly
    """

    def __init__(self, species, assembly_quality, contigs_filename):
        """
        PARAMETERS:

            species (str): the name of the species
            assembly_quality (AssemblyQuality): an object encapsulating the quality of the assembly
            contigs_filename (str): the file name of the contigs output from the assembly
        """

        self.species = species
        self.assembly_quality = assembly_quality
        self.contigs_filename = contigs_filename
