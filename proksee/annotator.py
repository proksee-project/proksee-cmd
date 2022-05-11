"""
Copyright Government of Canada 2020

Written by:

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


class Annotator(ABC):
    """
    An abstract class representing a sequence annotator.

    ATTRIBUTES:
        name (str): the plain-language name of the annotator
        contigs_filepath (str): the filepath of the contigs to annotate
        output_directory (str): the filepath of the output directory
        resource_specification (ResourceSpecification): the resources that the annotator should use
    """

    def __init__(self, name, contigs_filepath, output_directory, resource_specification):
        """
        Initializes the abstract annotator.

        ATTRIBUTES:
            name (str): the plain-language name of the annotator
            contigs_filepath (str): the filepath of the contigs to annotate
            output_directory (str): the filepath of the output directory
            resource_specification (ResourceSpecification): the resources that the annotator should use
        """

        if not os.path.isfile(contigs_filepath):
            raise FileNotFoundError(str(contigs_filepath) + " not found.")

        self.name = name
        self.contigs_filepath = contigs_filepath
        self.output_directory = output_directory
        self.resource_specification = resource_specification

    @abstractmethod
    def annotate(self):
        """
        Annotates the contigs.

        POST
            If completed without error, the output will be placed in the output directory.
        """

        pass

    @abstractmethod
    def get_annotation_filename(self):
        """
        Gets the filename of the annotations.

        RETURNS
            filename (str): the filename of the annotations
        """
        pass
