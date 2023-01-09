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

from pathlib import Path

from proksee.contamination_handler import ContaminationHandler
from proksee.species import Species

TEST_MASH_DB_FILENAME = os.path.join(Path(__file__).parent.absolute(), "data", "ecoli.msh")
TEST_ID_MAPPING_FILENAME = os.path.join(Path(__file__).parent.absolute(), "data", "test_id_mapping.tab")


class TestContaminationHandler:

    def test_estimate_contamination(self):

        species = Species("Boletus subalpinus", 1.0)
        contigs_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "ecoli_mini.fasta")
        output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "testout")
        handler = ContaminationHandler(species, contigs_file, output_directory,
                                       TEST_MASH_DB_FILENAME, TEST_ID_MAPPING_FILENAME)

        evaluation = handler.estimate_contamination()

        print(evaluation.report)

        assert not evaluation.success

        message = "FAIL: The evaluated contigs don't appear to agree with the species estimation.\n"
        message += "      The estimated species is: " + str(species) + "\n"
        message += "      The following species were estimated from the contigs:\n\n"
        message += "      " + "Escherichia coli (p=1.00)"

        assert (evaluation.report == message)

    def test_no_contamination(self):

        species = Species("Escherichia coli", 1.0)
        contigs_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "ecoli_mini.fasta")
        output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "testout")
        handler = ContaminationHandler(species, contigs_file, output_directory,
                                       TEST_MASH_DB_FILENAME, TEST_ID_MAPPING_FILENAME)

        evaluation = handler.estimate_contamination()

        assert evaluation.success

        message = "PASS: The evaluated contigs appear to agree with the species estimation.\n"
        message += "      The estimated species is: " + str(species)

        assert (evaluation.report == message)

    def test_low_confidence_estimation(self):

        species = Species("Staphylococcus pseudintermedius", 1.0)
        contigs_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "simple_contig.fasta")
        output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "testout")
        handler = ContaminationHandler(species, contigs_file, output_directory,
                                       TEST_MASH_DB_FILENAME, TEST_ID_MAPPING_FILENAME)

        evaluation = handler.estimate_contamination()
        print(evaluation.report)

        assert evaluation.success

        message = "WARNING: Unable to confidently estimate the species from the assembled contigs."

        assert (evaluation.report == message)
