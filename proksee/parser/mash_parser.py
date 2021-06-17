"""
Copyright Government of Canada 2021

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
import copy

from proksee.species import Species
from proksee.species_estimation import Estimation


class MashParser:
    """
    This class represents a parser capable of taking the output from Mash and producing species Estimations.

    ATTRIBUTES
        taxonomy_mapping_filename (str): the filename of the file that maps NCBI accession IDs to taxonomic
            information, for every ID present in the Mash sketch file used to create the Mash output that
            will be parsed by this class.
    """

    def __init__(self, taxonomy_mapping_filename):
        """
        Initializes the Mash Parser.

        PARAMETERS:
            taxonomy_mapping_filename: filename of the NCBI ID-to-taxonomy mapping file
        """

        self.taxonomy_mapping_filename = taxonomy_mapping_filename

    def parse_estimations(self, mash_filename):
        """
        This function parses the output file of Mash's "screen" command. The input file should contain the full
        output from this command. This parser returns Estimations, with only minimal reduction of the data.

        Only one Estimation from each species (the first observed, with the highest identity) is maintained.

        PARAMETERS:
            mash_filename (str): the file location of the output from 'mash screen'

        RETURNS:
            estimations (List(Estimation)): a list of Estimation objects sorted from highest identity to lowest
        """

        # Index positions of parsed Mash tokens:
        IDENTITY = 0
        SHARED_HASHES = 1
        MEDIAN_MULTIPLICITY = 2
        PVALUE = 3
        QUERY_COMMENT = 5

        estimations = []

        if not os.path.exists(mash_filename):
            raise FileNotFoundError("File not found: " + mash_filename)

        # Make sure that the file contains data:
        if os.path.getsize(mash_filename) > 0:

            mapping = load_mapping_file(self.taxonomy_mapping_filename)

            with open(mash_filename) as file:

                for line in file:

                    tokens = line.strip().split("\t")

                    # ignore empty lines
                    if len(tokens) <= 1:
                        continue

                    confidence = 1 - float(tokens[PVALUE])  # inverse because pvalue relates to prob of accidental match
                    identity = float(tokens[IDENTITY])
                    shared_hashes_tokens = tokens[SHARED_HASHES].split("/")
                    shared_hashes = float(shared_hashes_tokens[0]) / float(shared_hashes_tokens[1])
                    median_multiplicity = int(tokens[MEDIAN_MULTIPLICITY])
                    query_comment = str(tokens[QUERY_COMMENT])

                    id = parse_ID_from_query_comment(query_comment)
                    id = id.split(".")[0]  # Removes the version number

                    species = copy.deepcopy(mapping[id])
                    # Deep copy because we don't want all references pointing to the same object
                    # when such objects might have the same species, but different confidences.

                    species.confidence = confidence  # Confidence must be updated
                    estimation = Estimation(species, identity, shared_hashes, median_multiplicity)

                    if estimation not in estimations:
                        estimations.append(estimation)

        return estimations


def parse_ID_from_query_comment(comment):
    """
    Parses the NCBI-specific ID from the comment reported by the Mash match. The comment will look something like:

    [1870 seqs] NC_004354.4 Drosophila melanogaster chromosome X [...]

    and this function will return the "NC_004354.4" part of the comment. This function is -VERY- specific to the
    formatting of a particular Mash (RefSeq) database.

    PARAMETERS:
        comment (str): the query comment to parse

    RETURNS:
        id (str): the NCBI-specific ID parsed from the passed comment
    """

    line = comment.strip()

    # Check for the optional [# seqs] at the start of line:
    if line.startswith("["):
        tokens = line.split("] ")
        line = tokens[1].strip()  # Grabbing everything after the "[# seqs] "

    id = line.split(" ")[0]

    return id


def load_mapping_file(mapping_filename):
    """
    Loads the NCBI ID-to-taxonomy mapping file into a hashable dictionary for easy lookup. The mapping file will be
    of the following format (seperated by tabs):

    NC_000001       9606    Homo sapiens    -       Homo    Hominidae       Primates        Mammalia        [...]
    NC_006468       9598    Pan troglodytes -       Pan     Hominidae       Primates        Mammalia        [...]

    PARAMETERS:
        mapping_filename (str): the filename of the mapping file

    RETURNS:
        mapping (dict(str->str)): a dictionary mapping NCBI IDs to species names
    """

    ID = 0
    SCIENTIFIC_NAME = 2
    SPECIES_NAME = 3
    SUPERKINGDOM = 10
    FULL_LINEAGE = 11

    MISSING = "-"

    mapping = {}

    with open(mapping_filename) as mapping_file:

        for line in mapping_file:

            tokens = line.split("\t")

            id = tokens[ID]
            species_name = tokens[SPECIES_NAME]

            # If there is a species name, use it, otherwise use the scientific name
            # The scientific name will be the species name when species name is missing
            if species_name == MISSING:
                species_name = tokens[SCIENTIFIC_NAME]

            superkingdom = tokens[SUPERKINGDOM]
            full_lineage = tokens[FULL_LINEAGE]
            species = Species(species_name, 0.0, superkingdom=superkingdom, full_lineage=full_lineage)

            mapping[id] = species

    return mapping
