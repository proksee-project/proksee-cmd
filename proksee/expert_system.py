"""
Copyright Government of Canada 2020

Written by:

Eric Marinier
    National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from proksee.assembly_evaluator import evaluate_assembly, evaluate_assembly_from_fallback
from proksee.assembly_strategy import AssemblyStrategy
from proksee.skesa_assembler import SkesaAssembler
from proksee.spades_assembler import SpadesAssembler


class ExpertSystem:
    """
    A class representing an expert system for evaluating read or assembly data and deciding how to perform a
        high-quality assembly.

    ATTRIBUTES
        platform (str): the sequence platform used to sequence the reads
        species (species): the species to be assembled
        forward (str): the filename of the forward reads to be assembled
        reverse (str): the filename of the reverse reads to be assembled
        output_directory (str): the directory to use for program output
    """

    def __init__(self, platform, species, forward, reverse, output_directory):
        """
        Initializes the expert system.

        PARAMETERS
            platform (str): the sequence platform used to sequence the reads
            species (species): the species to be assembled
            forward (str): the filename of the forward reads to be assembled
            reverse (str): the filename of the reverse reads to be assembled
            output_directory (str): the directory to use for program output
        """

        self.platform = platform
        self.species = species
        self.forward = forward
        self.reverse = reverse
        self.output_directory = output_directory

        return

    def create_fast_assembly_strategy(self, read_quality):
        """
        PARAMETERS
            read_quality (ReadQuality): an object encapsulating information about read quality

        RETURNS
            strategy (AssemblyStrategy): an assembly strategy, based on the information about the reads
        """

        MIN_Q20_RATE = 0.60

        proceed = True
        report = ""

        if read_quality.q20_rate < MIN_Q20_RATE:
            proceed = False

            report += "The read quality is too low.\n"
            report += "The rate of Q20 bases is: " + str(read_quality.q20_rate) + "\n"

        else:
            report += "The read quality is acceptable.\n"

        assembler = SkesaAssembler(self.forward, self.reverse, self.output_directory)

        return AssemblyStrategy(proceed, assembler, report)

    def create_full_assembly_strategy(self, assembly_quality, assembly_database):
        """
        Creates a full assembly strategy by comparing the assembly quality and species to statistical information in an
        assembly database about similar assemblies.

        PARAMETERS
            assembly_quality (AssemblyQuality): an object representing the quality of an assembly
            assembly_database (AssemblyDatabase): an object containing assembly statistics for various species

        RETURN
            strategy (AssemblyStrategy): a strategy for assembly, based on the information provided from a
                previous assembly
        """

        species_name = self.species.name

        if assembly_database.contains(species_name):

            evaluation = evaluate_assembly(self.species, assembly_quality, assembly_database)

            assembler = SpadesAssembler(self.forward, self.reverse, self.output_directory)
            strategy = AssemblyStrategy(evaluation.proceed, assembler, evaluation.report)

        else:

            strategy = self.create_fallback_assembly_strategy(assembly_quality)

        return strategy

    def create_fallback_assembly_strategy(self, assembly_quality):
        """
        Creates a fallback assembly strategy, to be used when the species is unidentifiable or not present in the
        assembly database.

        PARAMETERS
            assembly_quality (AssemblyQuality): an object representing the quality of an assembly

        RETURN
            strategy (AssemblyStrategy): a strategy for assembly, based on the information provided from a
                previous assembly
        """

        evaluation = evaluate_assembly_from_fallback(assembly_quality)

        assembler = SpadesAssembler(self.forward, self.reverse, self.output_directory)
        strategy = AssemblyStrategy(evaluation.proceed, assembler, evaluation.report)

        return strategy
