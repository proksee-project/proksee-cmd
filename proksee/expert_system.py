"""
Copyright Government of Canada 2020

Written by:

Arnab Saha Mandal
    University of Manitoba
    National Microbiology Laboratory, Public Health Agency of Canada

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
        """

        return

    def evaluate_assembly(self, assembly_quality, assembly_database):
        """
        PARAMETERS
            assembly_quality (AssemblyQuality): An object representing the quality of an assembly.
            assembly_database (AssemblyDatabase): An object containing assembly statistics for various species.
        """

        species_name = self.species.name

        if assembly_database.contains(species_name):

            n50 = assembly_quality.n50
            n50_mean = assembly_database.get_n50_mean(species_name)
            n50_std = assembly_database.get_n50_std(species_name)

            z = (n50 - n50_mean) / n50_std
            p = stats.norm.cdf(z)

            if z > 0:
                p = 1 - p
                print("We expect {0:.0%} similar assemblies would have a greater N50.".format(p))

            else:
                print("We except {0:.2%} similar assemblies would have a smaller N50.".format(p))

        else:

            print(self.species.name + " is not present in the database.")

        return
