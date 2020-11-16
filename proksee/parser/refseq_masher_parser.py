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

import os

from proksee.species import Species


def parse_species_from_refseq_masher(refseq_masher_file):
    """
    This functions parses the output file of RefSeq Masher's "contains" command. The input file should contain the full
    output from this command. This parser returns classifications, with only minimal reduction of the data.

    This function expects the RefSeq Masher file to be sorted by identity in descending order. Only one classification
    from each species (the first observed, with the highest identity) is maintained.

    PARAMETERS:

        refseq_masher_file (str): the file location of the output from 'refseq_masher contains'

    RETURNS:

        classifications (List(Classification)): a list of classification objects sorted from highest identity to lowest
    """

    IDENTITY = 2
    SHARED_HASHES = 3
    MEDIAN_MULTIPLICITY = 4
    PVALUE = 5
    FULL_TAXONOMY = 6
    TAXONOMIC_SPECIES = 8

    classifications = []

    # Make sure that the file exists and contains data:
    if os.path.isfile(refseq_masher_file) and os.path.getsize(refseq_masher_file) > 0:

        with open(refseq_masher_file) as file:

            next(file)  # Skip the header line in the file.

            for line in file:

                tokens = line.strip().split("\t")

                # ignore empty lines
                if len(tokens) <= 1:
                    continue

                name = str(tokens[TAXONOMIC_SPECIES])
                confidence = 1 - float(tokens[PVALUE])  # inverse because pvalue relates to prob of accidental match

                identity = float(tokens[IDENTITY])
                shared_hashes_tokens = tokens[SHARED_HASHES].split("/")
                shared_hashes = float(shared_hashes_tokens[0]) / float(shared_hashes_tokens[1])
                median_multiplicity = int(tokens[MEDIAN_MULTIPLICITY])
                full_taxonomy = str(tokens[FULL_TAXONOMY])

                species = Species(name, confidence)
                classification = Classification(species, identity, shared_hashes, median_multiplicity, full_taxonomy)

                if classification not in classifications:
                    classifications.append(classification)

    return classifications


class Classification:
    """
    This class represents a RefSeq Masher "classification" of a species found in the input data.

    ATTRIBUTES
        species (Species): the species object representing the species
        identity (float): an estimation of what fraction of bases are shared between the genome of the species and the
            input data (estimated from the fraction of shared k-mers)
        shared_hashes (float): what fraction of the k-mer hashes were shared
        median_multiplicity (int): an estimation of coverage in the input data
        full_taxonomy (string): a full string name of the taxonomy
    """

    def __init__(self, species, identity, shared_hashes, median_multiplicity, full_taxonomy):
        """
        Initializes the classification.

        PARAMETERS
            species (Species): the species object representing the species
            identity (float): an estimation of what fraction of bases are shared between the genome of the species and
                the input data (estimated from the fraction of shared k-mers)
            shared_hashes (float): what fraction of the k-mer hashes were shared
            median_multiplicity (int): an estimation of coverage in the input data
            full_taxonomy (string): a full string name of the taxonomy
        """

        self.species = species
        self.identity = float(identity)
        self.shared_hashes = float(shared_hashes)
        self.median_multiplicity = int(median_multiplicity)
        self.full_taxonomy = str(full_taxonomy)

    def __eq__(self, other):
        """
        Replaces the default equals function.
        """

        return self.species.name == other.species.name
