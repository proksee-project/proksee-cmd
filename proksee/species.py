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


class Species:
    """
    A class representing a biological species.

    ATTRIBUTES
        name (str): the name of the species
        confidence (float): the confidence of the species assignment, between 0 and 1
    """

    UNKNOWN = "Unknown"  # The name to use when the species is unknown.

    def __init__(self, name, confidence):
        """
        Initializes the species.

        PARAMETERS
            name (str): the name of the species.
            confidence (float): the confidence of the species assignment, between 0 and 1
        """

        self.name = name
        self.confidence = confidence

    def __str__(self):
        """
        Replaces the default string function with one that is more informative.
        """

        return str(self.name) + " (p={:.2f})".format(self.confidence)

    def __repr__(self):
        """
        Replaces the default representation function with one that is more informative.
        """

        return str(self.name) + " (" + str(self.confidence) + ")"

    def __eq__(self, other):
        """
        Replaces the default equals function.
        """

        return self.name == other.name

    def __hash__(self):
        """
        Replaces the default hash function.
        """

        return self.name.__hash__()
