"""
Copyright Government of Canada 2020-2021

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

import csv
import json
import os

from proksee import __version__ as version

from proksee.version import FASTP_VERSION, QUAST_VERSION, SKESA_VERSION, SPADES_VERSION, MASH_VERSION

from proksee.database.version import MODEL_VERSION, NORM_DATABASE_VERSION
from proksee.heuristic_evaluator import REFSEQ_MIN_N50, REFSEQ_MAX_L50, REFSEQ_MAX_CONTIGS, REFSEQ_MIN_LENGTH
from proksee.heuristic_evaluator import EvaluationType


class AssemblyStatisticsWriter:
    """
    A class for writing assembly statistics to file.

    ATTRIBUTES
        output_directory (str): the location of the output directory
    """

    def __init__(self, output_directory):
        """
        Initializes the assembly statistics writer.

        PARAMETERS
            output_directory (str): the location of the directory to write output files

        POST
            The output directory will be created if it is missing.
        """

        self.output_directory = output_directory

        if not os.path.isdir(output_directory):
            os.mkdir(output_directory)

    def write_csv(self, names, qualities):
        """
        Writes the assembly statistics to a CSV output file.

        PARAMETERS
            names (List(str)): a list of names of the assemblies; should be the same length as qualities
            qualities (List(AssemblyQuality)): a list of AssemblyQuality objects; should be the same length as names

        RETURN
            output_filename (str): the name of the written file

        POST
            The assembly statistics will be written to the output file.
        """

        output_filename = os.path.join(self.output_directory, "assembly_statistics.csv")

        with open(output_filename, "w") as csvfile:

            ASSEMBLY_NAME = "Assembly Name"
            NUM_CONTIGS = "Number of Contigs"
            N50 = "N50"
            L50 = "L50"
            GC_CONTENT = "GC Content"
            LENGTH = "Length"

            csv_writer = csv.writer(csvfile, delimiter=',')

            headers = [ASSEMBLY_NAME, NUM_CONTIGS, N50, L50, GC_CONTENT, LENGTH]
            csv_writer.writerow(headers)

            for i in range(len(names)):
                name = names[i]
                quality = qualities[i]

                row = [name, quality.num_contigs, quality.n50, quality.l50, quality.gc_content, quality.length]
                csv_writer.writerow(row)

            return output_filename

    def write_json(self, platform, species, reads, read_quality, assembly_quality,
                   heuristic_evaluation, machine_learning_evaluation, database):
        """
        Writes the assembly information to a JSON file.

        PARAMETERS
            platform (Platform (Enum)): the sequencing platform
            species (Species): the sequencing species
            reads (Reads): encapsulates the file names of the input reads
            read_quality (ReadQuality): object encapsulating the quality measurements of the sequencing reads
            assembly_quality (AssemblyQuality): object encapsulating the quality measurements of the assembly
            heuristic_evaluation (AssemblyEvaluation): heuristic evaluation of the assembly
            machine_learning_evaluation (MachineLearningEvaluation): machine learning evaluation of the assembly
            database (AssemblyDatabase): database containing information about assemblies for species

        RETURN
            output_filename (str): the name of the written file

        POST
            The assembly information will be written to the output file.
        """

        output_filename = os.path.join(self.output_directory, "assembly_info.json")

        data = {}

        data['Version'] = {
            "Proksee": version,
            "Model": MODEL_VERSION,
            "Database": NORM_DATABASE_VERSION,
            "fastp": FASTP_VERSION,
            "SKESA": SKESA_VERSION,
            "QUAST": QUAST_VERSION,
            "SPAdes": SPADES_VERSION,
            "Mash": MASH_VERSION
        }

        data['Technology'] = str(platform.value)
        data['Species'] = species.name

        data["Reads"] = {
            "Forward": reads.forward,
            "Reverse": reads.reverse
        }

        data['Read Quality'] = {
            "Total Reads": read_quality.total_reads,
            "Total Bases": read_quality.total_bases,
            "Q20 Bases": read_quality.q20_bases,
            "Q20 Rate": read_quality.q20_rate,
            "Q30 Bases": read_quality.q30_bases,
            "Q30 Rate": read_quality.q30_rate,
            "GC Content": read_quality.gc_content
        }

        data['Assembly Quality'] = {
            "N50": assembly_quality.n50,
            "L50": assembly_quality.l50,
            "Number of Contigs": assembly_quality.num_contigs,
            "Assembly Size": assembly_quality.length
        }

        # Heuristic Evaluation used the species-specific method:
        if heuristic_evaluation.evaluation_type is EvaluationType.SPECIES:
            data['Heuristic Evaluation'] = {
                "Evaluation Method": "Species",
                "Success": heuristic_evaluation.success,
                "N50 Pass": heuristic_evaluation.n50_evaluation.success,
                "N50 Report": heuristic_evaluation.n50_evaluation.report,
                "Contigs Pass": heuristic_evaluation.contigs_evaluation.success,
                "Contigs Report": heuristic_evaluation.contigs_evaluation.report,
                "L50 Pass": heuristic_evaluation.l50_evaluation.success,
                "L50 Report": heuristic_evaluation.l50_evaluation.report,
                "Length Pass": heuristic_evaluation.length_evaluation.success,
                "Length Report": heuristic_evaluation.length_evaluation.report
            }

            data['Assembly Thresholds'] = {
                "Species Counts": database.get_count(species.name),
                "N50 Low Error": database.get_n50_quantile(species.name, database.LOW_ERROR_QUANTILE),
                "N50 Low Warning": database.get_n50_quantile(species.name, database.LOW_WARNING_QUANTILE),
                "N50 Median": database.get_n50_quantile(species.name, database.MEDIAN),
                "N50 High Warning": database.get_n50_quantile(species.name, database.HIGH_WARNING_QUANTILE),
                "N50 High Error": database.get_n50_quantile(species.name, database.HIGH_ERROR_QUANTILE),
                "L50 Low Error": database.get_l50_quantile(species.name, database.LOW_ERROR_QUANTILE),
                "L50 Low Warning": database.get_l50_quantile(species.name, database.LOW_WARNING_QUANTILE),
                "L50 Median": database.get_l50_quantile(species.name, database.MEDIAN),
                "L50 High Warning": database.get_l50_quantile(species.name, database.HIGH_WARNING_QUANTILE),
                "L50 High Error": database.get_l50_quantile(species.name, database.HIGH_ERROR_QUANTILE),
                "Contigs Low Error": database.get_contigs_quantile(species.name, database.LOW_ERROR_QUANTILE),
                "Contigs Low Warning": database.get_contigs_quantile(species.name, database.LOW_WARNING_QUANTILE),
                "Contigs Median": database.get_contigs_quantile(species.name, database.MEDIAN),
                "Contigs High Warning": database.get_contigs_quantile(species.name, database.HIGH_WARNING_QUANTILE),
                "Contigs High Error": database.get_contigs_quantile(species.name, database.HIGH_ERROR_QUANTILE),
                "Length Low Error": database.get_length_quantile(species.name, database.LOW_ERROR_QUANTILE),
                "Length Low Warning": database.get_length_quantile(species.name, database.LOW_WARNING_QUANTILE),
                "Length Median": database.get_length_quantile(species.name, database.MEDIAN),
                "Length High Warning": database.get_length_quantile(species.name, database.HIGH_WARNING_QUANTILE),
                "Length High Error": database.get_length_quantile(species.name, database.HIGH_ERROR_QUANTILE)
            }

        # Heuristic Evaluation used the fallback method:
        else:
            data['Heuristic Evaluation'] = {
                "Evaluation Method": "Fallback",
                "Success": heuristic_evaluation.success,
                "N50 Pass": heuristic_evaluation.n50_evaluation.success,
                "N50 Report": heuristic_evaluation.n50_evaluation.report,
                "Contigs Pass": heuristic_evaluation.contigs_evaluation.success,
                "Contigs Report": heuristic_evaluation.contigs_evaluation.report,
                "L50 Pass": heuristic_evaluation.l50_evaluation.success,
                "L50 Report": heuristic_evaluation.l50_evaluation.report,
                "Length Pass": heuristic_evaluation.length_evaluation.success,
                "Length Report": heuristic_evaluation.length_evaluation.report
            }

        data["NCBI RefSeq Exclusion Criteria"] = {
            "Minimum Length": REFSEQ_MIN_LENGTH,
            "Minimum N50": REFSEQ_MIN_N50,
            "Maximum L50": REFSEQ_MAX_L50,
            "Maximum Contigs": REFSEQ_MAX_CONTIGS
        }

        data['Machine Learning Evaluation'] = {
            "Success": machine_learning_evaluation.success,
            "Probability": machine_learning_evaluation.probability,
            "Report": machine_learning_evaluation.report
        }

        with open(output_filename, 'w') as output_file:
            json.dump(data, output_file, indent=4)

        return output_filename
