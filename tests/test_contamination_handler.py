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

from proksee.contamination_handler import ContaminationHandler
from proksee.species import Species


class TestContaminationHandler:

    def test_estimate_contamination(self):

        species = Species("Boletus subalpinus", 0.99999999290182)
        contigs_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "contamination.fasta")
        output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "testout")
        handler = ContaminationHandler(species, contigs_file, output_directory)

        evaluation = handler.estimate_contamination()

        assert not evaluation.success

        message = ""
        message += "FAIL: The evaluated contigs don't appear to agree with the species estimation.\n"
        message += "      The estimated species is: " + str(species) + "\n"
        message += "      The following species were estimated from the contigs:\n\n"
        message += "      " + "Boletus subalpinus (p=0.99999999290182)" + "\n"
        message += "      " + "Symphylella sp. YG-2006 (p=0.9999999291313)" + "\n"
        message += "      " + "Leuconostoc mesenteroides (p=0.999807514)" + "\n"

        assert(evaluation.report == message)

    def test_no_contamination(self):

        species = Species("Boletus subalpinus", 0.99999999290182)
        contigs_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "simple_contig.fasta")
        output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "testout")
        handler = ContaminationHandler(species, contigs_file, output_directory)

        evaluation = handler.estimate_contamination()

        assert evaluation.success

        message = ""
        message += "PASS: The evaluated contigs appear to agree with the species estimation.\n"
        message += "      The estimated species is: " + str(species) + "\n"

        assert(evaluation.report == message)
