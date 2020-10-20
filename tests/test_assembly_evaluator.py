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
import pytest

from proksee.assembly_evaluator import AssemblyEvaluator


class TestAssemblyEvaluator:

    def test_valid_contig_file(self):
        """
        Tests the AssemblyEvaluator with a valid contig file.
        """

        contigs_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "simple_contig.fasta")
        output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

        # Create a location for output, if it doesn't already exist:
        if not os.path.isdir(output_directory):
            os.mkdir(output_directory)

        assembly_evaluator = AssemblyEvaluator(contigs_filename, output_directory)
        assembly_evaluator.evaluate()

        assert os.path.isfile(assembly_evaluator.quast_report_filename)

    def test_missing_contig_file(self):
        """
        Tests the AssemblyEvaluator with a missing contig file. This should raise a FileNotFound exception.
        """

        missing_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "missing.file")
        output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

        # Create a location for output, if it doesn't already exist:
        if not os.path.isdir(output_directory):
            os.mkdir(output_directory)

        assembly_evaluator = AssemblyEvaluator(missing_filename, output_directory)

        with pytest.raises(FileNotFoundError):
            assembly_evaluator.evaluate()
