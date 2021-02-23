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

from proksee.assembly_database import AssemblyDatabase
from proksee.expert_system import ExpertSystem
from proksee.parser.assembly_quality_parser import parse_assembly_quality_from_quast_report
from proksee.parser.read_quality_parser import parse_read_quality_from_fastp
from proksee.reads import Reads
from proksee.species import Species

INPUT_DIR = os.path.join(Path(__file__).parent.absolute(), "data")
OUTPUT_DIR = TEST_INPUT_DIR = os.path.join(Path(__file__).parent.absolute(), "output")


class TestExpertSystem:

    def test_evaluate_good_reads(self):
        """
        Tests the expert system's evaluation of "good" reads.
        """

        platform = "Illumina"
        species = Species("Staphylococcus aureus", 1.0)
        forward = os.path.join(INPUT_DIR, "staph_mini.fastq")
        reverse = None
        reads = Reads(forward, reverse)
        FASTP_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data", "good_reads.json")

        system = ExpertSystem(platform, species, reads, OUTPUT_DIR)
        read_quality = parse_read_quality_from_fastp(FASTP_PATH)

        strategy = system.create_fast_assembly_strategy(read_quality)

        assert strategy.proceed

    def test_evaluate_bad_reads(self):
        """
        Tests the expert system's evaluation of "bad" reads.
        """

        platform = "Illumina"
        species = Species("Staphylococcus aureus", 1.0)
        forward = os.path.join(INPUT_DIR, "staph_mini.fastq")
        reverse = None
        reads = Reads(forward, reverse)
        FASTP_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data", "bad_reads.json")

        system = ExpertSystem(platform, species, reads, OUTPUT_DIR)
        read_quality = parse_read_quality_from_fastp(FASTP_PATH)

        strategy = system.create_fast_assembly_strategy(read_quality)

        assert not strategy.proceed

    def test_evaluate_good_assembly(self):
        """
        Tests the expert system's evaluation of a "good" assembly.
        """

        platform = "Illumina"
        species = Species("Staphylococcus aureus", 1.0)
        forward = os.path.join(INPUT_DIR, "staph_mini.fastq")
        reverse = None
        reads = Reads(forward, reverse)
        QUAST_FILENAME = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data", "good_assembly.tsv")
        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database",
                                     "refseq_short.csv")

        system = ExpertSystem(platform, species, reads, OUTPUT_DIR)
        assembly_quality = parse_assembly_quality_from_quast_report(QUAST_FILENAME)
        database = AssemblyDatabase(DATABASE_PATH)

        strategy = system.create_full_assembly_strategy(assembly_quality, database)
        print(strategy.report)
        assert strategy.proceed

    def test_evaluate_bad_assembly(self):
        """
        Tests the expert system's evaluation of a "bad" assembly.
        """

        platform = "Illumina"
        species = Species("Staphylococcus aureus", 1.0)
        forward = os.path.join(INPUT_DIR, "staph_mini.fastq")
        reverse = None
        reads = Reads(forward, reverse)
        QUAST_FILENAME = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data", "bad_assembly.tsv")
        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database",
                                     "refseq_short.csv")

        system = ExpertSystem(platform, species, reads, OUTPUT_DIR)
        assembly_quality = parse_assembly_quality_from_quast_report(QUAST_FILENAME)
        database = AssemblyDatabase(DATABASE_PATH)

        strategy = system.create_full_assembly_strategy(assembly_quality, database)

        assert not strategy.proceed

    def test_evaluate_assembly_too_big(self):
        """
        Tests the expert system's evaluation of an assembly that seems to be too large.
        """

        platform = "Illumina"
        species = Species("Staphylococcus aureus", 1.0)
        forward = os.path.join(INPUT_DIR, "staph_mini.fastq")
        reverse = None
        reads = Reads(forward, reverse)
        QUAST_FILENAME = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data", "big_assembly.tsv")
        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database",
                                     "refseq_short.csv")

        system = ExpertSystem(platform, species, reads, OUTPUT_DIR)
        assembly_quality = parse_assembly_quality_from_quast_report(QUAST_FILENAME)
        database = AssemblyDatabase(DATABASE_PATH)

        strategy = system.create_full_assembly_strategy(assembly_quality, database)

        assert not strategy.proceed

    def test_evaluate_assembly_missing_species(self):
        """
        Tests the expert system's evaluation when a species is not present in the database.
        """

        platform = "Illumina"
        species = Species("ABCDEFG987", 1.0)
        forward = os.path.join(INPUT_DIR, "staph_mini.fastq")
        reverse = None
        reads = Reads(forward, reverse)
        QUAST_FILENAME = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data", "good_assembly.tsv")
        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "proksee", "database",
                                     "refseq_short.csv")

        system = ExpertSystem(platform, species, reads, OUTPUT_DIR)
        assembly_quality = parse_assembly_quality_from_quast_report(QUAST_FILENAME)
        database = AssemblyDatabase(DATABASE_PATH)

        strategy = system.create_full_assembly_strategy(assembly_quality, database)

        assert strategy.proceed
