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
from proksee.species import Species


class TestExpertSystem:

    def test_evaluate_good_reads(self):
        """
        Tests the expert system's evaluation of "good" reads.
        """

        PLATFORM = "Illumina"
        SPECIES = Species("Staphylococcus aureus", 1.0)
        FASTP_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data", "good_reads.json")

        system = ExpertSystem(PLATFORM, SPECIES)
        read_quality = parse_read_quality_from_fastp(FASTP_PATH)

        strategy = system.evaluate_reads(read_quality)

        assert strategy.proceed

    def test_evaluate_bad_reads(self):
        """
        Tests the expert system's evaluation of "bad" reads.
        """

        PLATFORM = "Illumina"
        SPECIES = Species("Staphylococcus aureus", 1.0)
        FASTP_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data", "bad_reads.json")

        system = ExpertSystem(PLATFORM, SPECIES)
        read_quality = parse_read_quality_from_fastp(FASTP_PATH)

        strategy = system.evaluate_reads(read_quality)

        assert not strategy.proceed

    def test_evaluate_good_assembly(self):
        """
        Tests the expert system's evaluation of a "good" assembly.
        """

        PLATFORM = "Illumina"
        SPECIES = Species("Staphylococcus aureus", 1.0)
        QUAST_FILENAME = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data", "good_assembly.tsv")
        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                                     "database.csv")

        system = ExpertSystem(PLATFORM, SPECIES)
        assembly_quality = parse_assembly_quality_from_quast_report(QUAST_FILENAME)
        database = AssemblyDatabase(DATABASE_PATH)

        strategy = system.evaluate_assembly(assembly_quality, database)

        assert strategy.proceed

    def test_evaluate_bad_assembly(self):
        """
        Tests the expert system's evaluation of a "bad" assembly.
        """

        PLATFORM = "Illumina"
        SPECIES = Species("Staphylococcus aureus", 1.0)
        QUAST_FILENAME = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data", "bad_assembly.tsv")
        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                                     "database.csv")

        system = ExpertSystem(PLATFORM, SPECIES)
        assembly_quality = parse_assembly_quality_from_quast_report(QUAST_FILENAME)
        database = AssemblyDatabase(DATABASE_PATH)

        strategy = system.evaluate_assembly(assembly_quality, database)

        assert not strategy.proceed

    def test_evaluate_assembly_too_big(self):
        """
        Tests the expert system's evaluation of an assembly that seems to be too large.
        """

        PLATFORM = "Illumina"
        SPECIES = Species("Staphylococcus aureus", 1.0)
        QUAST_FILENAME = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data", "big_assembly.tsv")
        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                                     "database.csv")

        system = ExpertSystem(PLATFORM, SPECIES)
        assembly_quality = parse_assembly_quality_from_quast_report(QUAST_FILENAME)
        database = AssemblyDatabase(DATABASE_PATH)

        strategy = system.evaluate_assembly(assembly_quality, database)

        assert not strategy.proceed

    def test_evaluate_assembly_missing_species(self):
        """
        Tests the expert system's evaluation when a species is not present in the database.
        """

        PLATFORM = "Illumina"
        SPECIES = Species("ABCDEFG987", 1.0)
        QUAST_FILENAME = os.path.join(Path(__file__).parent.parent.absolute(), "tests", "data", "good_assembly.tsv")
        DATABASE_PATH = os.path.join(Path(__file__).parent.parent.absolute(), "database",
                                     "database.csv")

        system = ExpertSystem(PLATFORM, SPECIES)
        assembly_quality = parse_assembly_quality_from_quast_report(QUAST_FILENAME)
        database = AssemblyDatabase(DATABASE_PATH)

        strategy = system.evaluate_assembly(assembly_quality, database)

        assert not strategy.proceed
