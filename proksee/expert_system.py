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
        report = ""

        if assembly_database.contains(species_name):

            n50_evaluation = self.evaluate_n50(assembly_quality, assembly_database)
            proceed = n50_evaluation.success
            report += n50_evaluation.report

        else:
            proceed = False

            report += self.species.name + " is not present in the database.\n"

        assembler = SpadesAssembler(self.forward, self.reverse, self.output_directory)

        return AssemblyStrategy(proceed, assembler, report)

    def evaluate_n50(self, assembly_quality, assembly_database):
        """
        Evaluates the N50 of the passed AssemblyQuality against the assembly statistics for the given species in the
        assembly database.

        PARAMETERS
            assembly_quality (AssemblyQuality): an object representing the quality of an assembly
            assembly_database (AssemblyDatabase): an object containing assembly statistics for various species

        RETURN
            evaluation (Evaluation): an evaluation of the N50 against the assembly database
        """

        species_name = self.species.name
        report = ""

        n50 = assembly_quality.n50
        n50_20 = assembly_database.get_n50_quantile(species_name, 0.20)
        n50_80 = assembly_database.get_n50_quantile(species_name, 0.80)

        if n50_20 <= n50 <= n50_80:
            success = True
            report += "The N50 is comparable to similar assemblies: {}\n".format(n50)
            report += "The acceptable N50 range is: [{}, {}]\n".format(n50_20, n50_80)

        elif n50 < n50_20:
            success = False
            report += "The N50 is smaller than expected: {}\n".format(n50)
            report += "The N50 lower bound is: {}\n".format(n50_20)

        else:
            success = False
            report += "The N50 is larger than expected: {}\n".format(n50)
            report += "The N50 upper bound is: {}\n".format(n50_80)

        evaluation = self.Evaluation(success, report)

        return evaluation

    class Evaluation:
        """
        A class representing a simple evaluation of a test.

        ATTRIBUTES
            success (bool): whether or not the test was passed
            report (str): a plain-language String describing the evaluation
        """

        def __init__(self, success, report):
            """
            Initializes the Evaluation.

            PARAMETERS
                success (bool): whether or not the test was passed
                report (str): a plain-language String describing the evaluation
            """
            self.success = success
            self.report = report
