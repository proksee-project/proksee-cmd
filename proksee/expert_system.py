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


class ExpertSystem:
    """
    A class representing an expert system for evaluating read or assembly data and deciding how to perform a
        high-quality assembly.

    ATTRIBUTES
        platform (str): The sequence platform used to sequence the reads.
        species (species): The species to be assembled.
    """

    def __init__(self, platform, species):
        """
        Initializes the expert system.

        PARAMETERS
            platform (str): The sequence platform used to sequence the reads.
            species (species): The species to be assembled.
        """

        self.platform = platform
        self.species = species

        return

    def evaluate_reads(self, read_quality):
        """
        PARAMETERS
            read_quality (ReadQuality): An object encapsulating information about read quality.

        RETURNS
            strategy (AssemblyStrategy): An assembly strategy, based on the information about the reads.
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

        return AssemblyStrategy(proceed, report)

    def evaluate_assembly(self, assembly_quality, assembly_database):
        """
        Evaluates the assembly by comparing it to statistical information in an assembly database about similar
            assemblies.

        PARAMETERS
            assembly_quality (AssemblyQuality): An object representing the quality of an assembly.
            assembly_database (AssemblyDatabase): An object containing assembly statistics for various species.

        RETURN
            strategy (AssemblyStrategy): A strategy for assembly, based on the information provided from a
                previous assembly.
        """

        species_name = self.species.name
        proceed = True
        report = ""

        if assembly_database.contains(species_name):

            n50 = assembly_quality.n50
            n50_20 = assembly_database.get_n50_20(species_name)
            n50_80 = assembly_database.get_n50_80(species_name)

            if n50_20 <= n50 <= n50_80:
                report += "The N50 is comparable to similar assemblies.\n"

            elif n50 < n50_20:
                proceed = False

                report += "The N50 is smaller than expected: {}\n".format(n50)

            else:
                proceed = False

                report += "The N50 is larger than expected: {}\n".format(n50)

        else:
            proceed = False

            report += self.species.name + " is not present in the database.\n"

        return AssemblyStrategy(proceed, report)
