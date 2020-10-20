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


class ExpertSystem:
    """
    A class representing an expert system for evaluating assembly data and deciding how to perform a high-quality
    assembly.

    ATTRIBUTES
        platform (str): The sequence platform used to sequence the reads.
        organism (str): The name of the organism to be assembled.
        read_quality (ReadQuality): A ReadQuality object encapsulating information about read quality.
    """

    def __init__(self, platform, organism, read_quality):
        """
        Initializes the expert system.

        PARAMETERS
            platform (str): The sequence platform used to sequence the reads.
            organism (str): The name of the organism to be assembled.
            read_quality (ReadQuality): A ReadQuality object encapsulating information about read quality.
        """

        self.platform = platform
        self.organism = organism
        self.read_quality = read_quality

        return
