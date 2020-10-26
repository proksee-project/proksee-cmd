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

from abc import ABC, abstractmethod


class Assembler(ABC):
    """
    An abstract class representing a sequence assembler.

    ATTRIBUTES:
        forward (str): the filename of the forward reads
        reverse (str): the filename of the reverse reads
        output_dir (str): the filename of the output directory
        contigs_filename (str): the filename of the assembled contigs
        log_filename (str): the filename of the logfile
    """

    # Defining __init__ method with reads and output directory parameters
    def __init__(self, forward, reverse, output_dir):
        self.forward = forward
        self.reverse = reverse
        self.output_dir = output_dir
        self.contigs_filename = ""
        self.log_filename = ""

    @abstractmethod
    def assemble(self):
        pass
