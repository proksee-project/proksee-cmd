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
from proksee.species_estimation import Estimation


def parse_estimations_from_file(refseq_masher_file):
    """
    This function parses the output file of RefSeq Masher's "contains" command. The input file should contain the full
    output from this command. This parser returns Estimations, with only minimal reduction of the data.

    This function expects the RefSeq Masher file to be sorted by identity in descending order. Only one Estimation
    from each species (the first observed, with the highest identity) is maintained.

    PARAMETERS:

        refseq_masher_file (str): the file location of the output from 'refseq_masher contains'

    RETURNS:

        estimations (List(Estimation)): a list of Estimation objects sorted from highest identity to lowest
    """

    IDENTITY = "identity"
    SHARED_HASHES = "shared_hashes"
    MEDIAN_MULTIPLICITY = "median_multiplicity"
    PVALUE = "pvalue"
    FULL_TAXONOMY = "full_taxonomy"
    TAXONOMIC_SPECIES = "taxonomic_species"

    estimations = []

    if not os.path.exists(refseq_masher_file):
        raise FileNotFoundError("File not found: " + refseq_masher_file)

    # Make sure that the file contains data:
    if os.path.getsize(refseq_masher_file) > 0:

        with open(refseq_masher_file) as file:

            # Determine the positions of columns from the header line.
            # These columns do not always have the same positions!
            # (Some outputs may be missing the taxonomic_subspecies column!)
            headers = file.readline().split()

            identity_pos = headers.index(IDENTITY)
            shared_hashes_pos = headers.index(SHARED_HASHES)
            median_multiplicity_pos = headers.index(MEDIAN_MULTIPLICITY)
            pvalue_pos = headers.index(PVALUE)
            full_taxonomy_pos = headers.index(FULL_TAXONOMY)
            taxonomic_species_pos = headers.index(TAXONOMIC_SPECIES)

            for line in file:

                tokens = line.strip().split("\t")

                # ignore empty lines
                if len(tokens) <= 1:
                    continue

                name = str(tokens[taxonomic_species_pos])
                confidence = 1 - float(tokens[pvalue_pos])  # inverse because pvalue relates to prob of accidental match

                identity = float(tokens[identity_pos])
                shared_hashes_tokens = tokens[shared_hashes_pos].split("/")
                shared_hashes = float(shared_hashes_tokens[0]) / float(shared_hashes_tokens[1])
                median_multiplicity = int(tokens[median_multiplicity_pos])
                full_taxonomy = str(tokens[full_taxonomy_pos])

                species = Species(name, confidence)
                estimation = Estimation(species, identity, shared_hashes, median_multiplicity, full_taxonomy)

                if estimation not in estimations:
                    estimations.append(estimation)

    return estimations


def parse_estimations_from_dataframe(dataframe):
    """
    This function parses the dataframe output from the RefSeq Masher (RSM) "contains" command, after RSM as has
    merged NCBI taxonomy info and ordered the output columns. This parser returns Estimations, with only minimal
    reduction of the data.

    This function expects the RefSeq Masher dataframe to be sorted by identity in descending order. Only one
    Estimation from each species (the first observed, with the highest identity) is maintained.

    PARAMETERS:

        dataframe (pandas.DataFrame): the dataframe output from 'refseq_masher contains' (NCBI merged and sorted)

    RETURNS:

        estimations (List(Estimation)): a list of Estimation objects sorted from highest identity to lowest
    """

    IDENTITY = "identity"
    SHARED_HASHES = "shared_hashes"
    MEDIAN_MULTIPLICITY = "median_multiplicity"
    PVALUE = "pvalue"
    FULL_TAXONOMY = "full_taxonomy"
    TAXONOMIC_SPECIES = "taxonomic_species"

    estimations = []

    for index, row in dataframe.iterrows():

        name = row[TAXONOMIC_SPECIES]
        confidence = 1 - float(row[PVALUE])  # inverse because pvalue relates to prob of accidental match

        identity = float(row[IDENTITY])
        shared_hashes_tokens = row[SHARED_HASHES].split("/")
        shared_hashes = float(shared_hashes_tokens[0]) / float(shared_hashes_tokens[1])
        median_multiplicity = int(row[MEDIAN_MULTIPLICITY])
        full_taxonomy = str(row[FULL_TAXONOMY])

        species = Species(name, confidence)
        estimation = Estimation(species, identity, shared_hashes, median_multiplicity, full_taxonomy)

        if estimation not in estimations:
            estimations.append(estimation)

    return estimations
