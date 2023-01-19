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

from proksee.assembly_strategy import AssemblyStrategy
from proksee.species_assembly_evaluator import SpeciesAssemblyEvaluator
from proksee.ncbi_assembly_evaluator import NCBIAssemblyEvaluator
from proksee.skesa_assembler import SkesaAssembler
from proksee.spades_assembler import SpadesAssembler


class ExpertSystem:
    """
    A class representing an expert system for evaluating read or assembly data and deciding how to perform a
        high-quality assembly.

    ATTRIBUTES
        platform (str): the sequence platform used to sequence the reads
        species (species): the species to be assembled
        reads (Reads): the reads to assemble
        output_directory (str): the directory to use for program output
        resource_specification (ResourceSpecification): the resources that sub-programs should use
    """

    def __init__(self, platform, species, reads, output_directory, resource_specification):
        """
        Initializes the expert system.

        PARAMETERS
            platform (str): the sequence platform used to sequence the reads
            species (species): the species to assemble
            reads (Reads): the reads to assemble
            output_directory (str): the directory to use for program output
            resource_specification (ResourceSpecification): the resources that sub-programs should use
        """

        self.platform = platform
        self.species = species
        self.reads = reads
        self.output_directory = output_directory
        self.resource_specification = resource_specification

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
            report += "The rate of Q20 bases is: " + str(read_quality.q20_rate)

        else:
            report += "The read quality is acceptable."

        assembler = SkesaAssembler(self.reads, self.output_directory, self.resource_specification)

        return AssemblyStrategy(proceed, assembler, report)

    def create_expert_assembly_strategy(self, assembly_quality, assembly_database):
        """
        Creates an expert assembly strategy by comparing the assembly quality and species to statistical information in
        an assembly database about similar assemblies.

        PARAMETERS
            assembly_quality (AssemblyQuality): an object representing the quality of an assembly
            assembly_database (AssemblyDatabase): a database containing assembly statistics for various species

        RETURN
            strategy (AssemblyStrategy): a strategy for assembly
        """

        species_name = self.species.name

        if assembly_database.contains(species_name):

            evaluator = SpeciesAssemblyEvaluator(self.species, assembly_database)
            species_evaluation = evaluator.evaluate_assembly_from_database(assembly_quality)

            assembler = SpadesAssembler(self.reads, self.output_directory, self.resource_specification)
            proceed = species_evaluation.success  # proceed if evaluation was successful
            strategy = AssemblyStrategy(proceed, assembler, species_evaluation.report)

        else:

            strategy = self.create_fallback_assembly_strategy(assembly_quality, assembly_database)

        return strategy

    def create_fallback_assembly_strategy(self, assembly_quality, assembly_database):
        """
        Creates a fallback assembly strategy, to be used when the species is unidentifiable or not present in the
        assembly database.

        PARAMETERS
            assembly_quality (AssemblyQuality): an object representing the quality of an assembly
            assembly_database (AssemblyDatabase): a database containing assembly statistics for various species

        RETURN
            strategy (AssemblyStrategy): a strategy for assembly
        """

        ncbi_evaluator = NCBIAssemblyEvaluator(self.species, assembly_database)
        evaluation = ncbi_evaluator.evaluate(assembly_quality)

        assembler = SpadesAssembler(self.reads, self.output_directory, self.resource_specification)
        proceed = evaluation.success  # proceed if evaluation was successful
        strategy = AssemblyStrategy(proceed, assembler, evaluation.report)

        return strategy
