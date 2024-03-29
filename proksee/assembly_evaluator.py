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

from abc import ABC, abstractmethod


class AssemblyEvaluator(ABC):
    """
    An abstract class representing a sequence assembly evaluator.

    ATTRIBUTES:
        species (Species): the biological species
    """

    def __init__(self, species):
        """
        Initializes the abstract assembly evaluator.

        PARAMETERS:
            species (Species): the biological species assembled
        """

        self.species = species

    @abstractmethod
    def evaluate(self, assembly_quality):
        """
        Evaluates the assembly.

        PARAMETERS:
            assembly_quality (AssemblyQuality): the quality measurements of the assembly

        RETURN
            evaluation (Evaluation): an evaluation of the assembly's quality
        """

        pass
