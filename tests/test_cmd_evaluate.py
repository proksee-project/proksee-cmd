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

from pathlib import Path

from proksee.commands.cmd_evaluate import evaluate
import proksee.config as config

INPUT_DIR = os.path.join(Path(__file__).parent.absolute(), "data")
OUTPUT_DIR = os.path.join(Path(__file__).parent.absolute(), "output")


class TestCmdEvaluate:

    def test_simple_evaluate(self):
        """
        Tests the cmd_evaluate.py's main control flow: .evaluate(...).
        This test uses data with a small file size, that is insufficient to
        test the accuracy of the evaluation. Instead, this data and test will
        be used to test the correctness of the program control flow.
        """

        contigs_filename = os.path.join(INPUT_DIR, "contamination.fasta")

        # Files being tracked:
        quast_file = os.path.join(OUTPUT_DIR, "quast", "report.txt")

        # Remove previous files if they exist:
        if os.path.isfile(quast_file):
            os.remove(quast_file)

        mash_database_path = config.get(config.MASH_PATH)
        evaluate(contigs_filename, OUTPUT_DIR, mash_database_path, species_name=None)

        # Check that expected files were created:
        assert os.path.isfile(quast_file)
