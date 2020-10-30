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
        report = "\n"

        if assembly_database.contains(species_name):

            n50_evaluation = self.evaluate_n50(assembly_quality, assembly_database)
            report += n50_evaluation.report

            contigs_evaluation = self.evaluate_num_contigs(assembly_quality, assembly_database)
            report += contigs_evaluation.report

            l50_evaluation = self.evaluate_l50(assembly_quality, assembly_database)
            report += l50_evaluation.report

            length_evaluation = self.evaluate_length(assembly_quality, assembly_database)
            report += length_evaluation.report

            proceed = n50_evaluation.success and contigs_evaluation.success \
                and l50_evaluation.success and length_evaluation.success

        else:
            proceed = False

            report += self.species.name + " is not present in the database.\n"

        assembler = SpadesAssembler(self.forward, self.reverse, self.output_directory)

        return AssemblyStrategy(proceed, assembler, report)

    def evaluate_value(self, measurement, value, low_fail, low_warning, high_warning, high_fail):
        """
        Evaluates a generic value for a measurement and reports whether or not it is within acceptable bounds.

        PARAMETERS
            measurement (str): plain-language name of the measurement (ex: "N50")
            value (comparable): the value to evaluate
            low_fail (comparable): the lower bound of failure
            low_warning (comparable): the lower bound for warning
            high_warning (comparable): the higher bound for warning
            high_fail (comparable): the higher bound of failure

        RETURNS
            evaluation (Evaluation): an evaluation of the measurement against the passed thresholds
        """

        report = ""

        # (-infinity, low_fail] -> low failure
        if value <= low_fail:
            success = False
            report += "FAIL: The {} is smaller than expected: {}\n".format(measurement, value)
            report += "\tThe {} lower bound is: {}\n".format(measurement, low_fail)

        # (low_fail, low_warning] -> low warning
        elif value <= low_warning:
            success = True
            report += "WARNING: The {} is somewhat smaller than expected: {}\n".format(measurement, value)
            report += "\tThe {} lower bound is: {}\n".format(measurement, low_fail)

        # (low_warning, high_warning) -> acceptable, no warning
        elif value < high_warning:
            success = True
            report += "PASS: The {} is comparable to similar assemblies: {}\n".format(measurement, value)
            report += "\tThe acceptable {} range is: ({}, {})\n".format(measurement, low_fail, high_fail)

        # [high_warning, high_fail) -> high warning
        elif value < high_fail:
            success = True
            report += "WARNING: The {} is somewhat larger than expected: {}\n".format(measurement, value)
            report += "\tThe {} upper bound is: {}\n".format(measurement, high_fail)

        # [high_fail, +infinity) -> high failure
        elif value >= high_fail:
            success = False
            report += "FAIL: The {} is larger than expected: {}\n".format(measurement, value)
            report += "\tThe {} upper bound is: {}\n".format(measurement, high_fail)

        evaluation = self.Evaluation(success, report)

        return evaluation

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

        n50 = assembly_quality.n50
        low_fail = assembly_database.get_n50_quantile(species_name, 0.05)
        low_warning = assembly_database.get_n50_quantile(species_name, 0.20)
        high_warning = assembly_database.get_n50_quantile(species_name, 0.80)
        high_fail = assembly_database.get_n50_quantile(species_name, 0.95)

        evaluation = self.evaluate_value("N50", n50, low_fail, low_warning, high_warning, high_fail)

        return evaluation

    def evaluate_num_contigs(self, assembly_quality, assembly_database):
        """
        Evaluates the number of contigs of the passed AssemblyQuality against the assembly statistics for the given
        species in the assembly database.

        PARAMETERS
            assembly_quality (AssemblyQuality): an object representing the quality of an assembly
            assembly_database (AssemblyDatabase): an object containing assembly statistics for various species

        RETURN
            evaluation (Evaluation): an evaluation of the number of contigs against the assembly database
        """

        species_name = self.species.name

        num_contigs = assembly_quality.num_contigs
        low_fail = assembly_database.get_contigs_quantile(species_name, 0.05)
        low_warning = assembly_database.get_contigs_quantile(species_name, 0.20)
        high_warning = assembly_database.get_contigs_quantile(species_name, 0.80)
        high_fail = assembly_database.get_contigs_quantile(species_name, 0.95)

        evaluation = self.evaluate_value("number of contigs", num_contigs, low_fail, low_warning, high_warning,
                                         high_fail)

        return evaluation

    def evaluate_l50(self, assembly_quality, assembly_database):
        """
        Evaluates the L50 of the passed AssemblyQuality against the assembly statistics for the given species in the
        assembly database.

        PARAMETERS
            assembly_quality (AssemblyQuality): an object representing the quality of an assembly
            assembly_database (AssemblyDatabase): an object containing assembly statistics for various species

        RETURN
            evaluation (Evaluation): an evaluation of the L50 against the assembly database
        """

        species_name = self.species.name

        l50 = assembly_quality.l50
        low_fail = assembly_database.get_l50_quantile(species_name, 0.05)
        low_warning = assembly_database.get_l50_quantile(species_name, 0.20)
        high_warning = assembly_database.get_l50_quantile(species_name, 0.80)
        high_fail = assembly_database.get_l50_quantile(species_name, 0.95)

        evaluation = self.evaluate_value("L50", l50, low_fail, low_warning, high_warning, high_fail)

        return evaluation

    def evaluate_length(self, assembly_quality, assembly_database):
        """
        Evaluates the assembly length of the passed AssemblyQuality against the assembly statistics for the given
        species in the assembly database.

        PARAMETERS
            assembly_quality (AssemblyQuality): an object representing the quality of an assembly
            assembly_database (AssemblyDatabase): an object containing assembly statistics for various species

        RETURN
            evaluation (Evaluation): an evaluation of the assembly length against the assembly database
        """

        species_name = self.species.name

        length = assembly_quality.length
        low_fail = assembly_database.get_length_quantile(species_name, 0.05)
        low_warning = assembly_database.get_length_quantile(species_name, 0.20)
        high_warning = assembly_database.get_length_quantile(species_name, 0.80)
        high_fail = assembly_database.get_length_quantile(species_name, 0.95)

        evaluation = self.evaluate_value("assembly length", length, low_fail, low_warning, high_warning, high_fail)

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
