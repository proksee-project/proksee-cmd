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


class Estimation:
    """
    This class represents a modified Mash "estimation" of a species found in the input data.

    ATTRIBUTES
        species (Species): the Species object representing the species
        identity (float): an estimation of what fraction of bases are shared between the genome of the species and the
            input data (estimated from the fraction of shared k-mers)
        shared_hashes (float): what fraction of the k-mer hashes were shared
        median_multiplicity (int): an estimation of coverage in the input data
    """

    def __init__(self, species, identity, shared_hashes, median_multiplicity):
        """
        Initializes the Estimation.

        PARAMETERS
            species (Species): the Species object representing the species
            identity (float): an estimation of what fraction of bases are shared between the genome of the species and
                the input data (estimated from the fraction of shared k-mers)
            shared_hashes (float): what fraction of the k-mer hashes were shared
            median_multiplicity (int): an estimation of coverage in the input data
        """

        self.species = species
        self.identity = float(identity)
        self.shared_hashes = float(shared_hashes)
        self.median_multiplicity = int(median_multiplicity)

    def __eq__(self, other):
        """
        Replaces the default equals function.
        """

        return self.species.name == other.species.name
