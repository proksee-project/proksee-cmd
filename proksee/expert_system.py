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

import scipy.stats as stats

from proksee.assembly_strategy import AssemblyStrategy


class ExpertSystem:
    """
    A class representing an expert system for evaluating assembly data and deciding how to perform a high-quality
    assembly.

    ATTRIBUTES
        platform (str): The sequence platform used to sequence the reads.
        species (species): The species to make decisions about.
    """

    def __init__(self, platform, species):
        """
        Initializes the expert system.

        PARAMETERS
            platform (str): The sequence platform used to sequence the reads.
            species (species): The species to make decisions about.
        """

        self.platform = platform
        self.species = species

        return

    def evaluate_reads(self, read_quality):
        """
        PARAMETERS
            read_quality (ReadQuality): A ReadQuality object encapsulating information about read quality.

        RETURNS
            strategy (AssemblyStrategy): An assembly strategy, based on the information about the reads.
        """

        MIN_Q30_RATE = 0.80

        proceed = True
        report = ""

        if read_quality.q30_rate < MIN_Q30_RATE:
            proceed = False

            report += "The read quality is too low.\n"
            report += "The rate of Q30 bases is: " + str(read_quality.q30_rate) + "\n"

        else:
            report += "The read quality is acceptable.\n"

        return AssemblyStrategy(proceed, report)

    def evaluate_assembly(self, assembly_quality, assembly_database):
        """
        Evaluates the assembly by comparing it to statistical information about similar assemblies.

        PARAMETERS
            assembly_quality (AssemblyQuality): An object representing the quality of an assembly.
            assembly_database (AssemblyDatabase): An object containing assembly statistics for various species.

        RETURN
            strategy (AssemblyStrategy): The strategy for assembly, based on the information provided from a
                previous assembly.
        """

        N50_LOWER_THRESHOLD = 0.20
        N50_UPPER_THRESHOLD = 0.80

        species_name = self.species.name
        proceed = True
        report = ""

        if assembly_database.contains(species_name):

            n50 = assembly_quality.n50
            n50_mean = assembly_database.get_n50_mean(species_name)
            n50_std = assembly_database.get_n50_std(species_name)

            z = (n50 - n50_mean) / n50_std
            p = stats.norm.cdf(z)

            if N50_LOWER_THRESHOLD <= p <= N50_UPPER_THRESHOLD:
                report += "The N50 is comparable to similar assemblies.\n"

            elif p < N50_LOWER_THRESHOLD:
                proceed = False

                report += "The N50 is smaller than expected.\n"
                report += "We would except {0:.2%} of similar assemblies to have a smaller N50.\n".format(p)

            else:
                p = 1 - p
                proceed = False

                report += "The N50 is larger than expected.\n"
                report += "We would except {0:.2%} of similar assemblies to have a larger N50.\n".format(p)

        else:
            proceed = False

            report += self.species.name + " is not present in the database.\n"

        return AssemblyStrategy(proceed, report)
