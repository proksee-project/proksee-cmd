"""
Copyright Government of Canada 2020

Written by:

Arnab Saha Mandal
    University of Manitoba
    National Microbiology Laboratory, Public Health Agency of Canada

Eric Marinier
    National Microbiology Laboratory, Public Health Agency of Canada

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
from abc import ABC, abstractmethod


class Assembler(ABC):
    """
    An abstract class representing a sequence assembler.

    ATTRIBUTES:
        name (str): the plain-language name of the assembler
        reads (Reads): the reads to assemble
        output_dir (str): the filename of the output directory
        resource_specification (ResourceSpecification): the specification of resource that the assembler should use
    """

    def __init__(self, name, reads, output_dir, resource_specification):
        """
        Initializes the abstract assembler.

        ATTRIBUTES:
            name (str): the plain-language name of the assembler
            reads (Reads): the reads to assemble
            output_dir (str): the filename of the output directory
            resource_specification (ResourceSpecification): the specification of resource that the assembler should use
        """

        if not os.path.isfile(reads.forward):
            raise FileNotFoundError(str(reads.forward) + " not found.")

        self.name = name
        self.reads = reads
        self.output_dir = output_dir
        self.resource_specification = resource_specification

    @abstractmethod
    def assemble(self):
        """
        Assembles the reads.

        RETURNS
            output (str): an output string reporting the result back to the user

        POST
            If completed without error, the output will be placed in the output directory.
        """

        pass

    @abstractmethod
    def get_contigs_filename(self):
        """
        Gets the filename of the assembled contigs.

        RETURNS
            filename (str): the filename of the assembled contigs
        """
        pass
