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
from proksee.ncbi_assembly_evaluator import REFSEQ_MIN_N50, REFSEQ_MAX_L50, REFSEQ_MAX_CONTIGS, REFSEQ_MIN_LENGTH


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
                   species_evaluation, machine_learning_evaluation, ncbi_evaluation, database):
        """
        Writes the assembly information to a JSON file.

        PARAMETERS
            platform (Platform (Enum)): the sequencing platform
            species (Species): the sequencing species
            reads (Reads): encapsulates the file names of the input reads
            read_quality (ReadQuality): object encapsulating the quality measurements of the sequencing reads
            assembly_quality (AssemblyQuality): object encapsulating the quality measurements of the assembly
            species_evaluation (AssemblyEvaluation): heuristic species-based evaluation of the assembly
            machine_learning_evaluation (MachineLearningEvaluation): machine learning evaluation of the assembly
            ncbi_evaluation (AssemblyEvaluation): heuristic ncbi fallback-based evaluation of the assembly
            database (AssemblyDatabase): database containing information about assemblies for species

        RETURN
            output_filename (str): the name of the written file

        POST
            The assembly information will be written to the output file.
        """

        output_filename = os.path.join(self.output_directory, "assembly_info.json")

        data = {}

        data['Version'] = {
            "proksee": version,
            "model": MODEL_VERSION,
            "database": NORM_DATABASE_VERSION,
            "fastp": FASTP_VERSION,
            "skesa": SKESA_VERSION,
            "quast": QUAST_VERSION,
            "spades": SPADES_VERSION,
            "mash": MASH_VERSION
        }

        data['technology'] = str(platform.value)
        data['species'] = species.name

        data["reads"] = {
            "forward": reads.forward,
            "reverse": reads.reverse
        }

        data['readQuality'] = {
            "totalReads": read_quality.total_reads,
            "totalBases": read_quality.total_bases,
            "q20Bases": read_quality.q20_bases,
            "q20Rate": read_quality.q20_rate,
            "q30Bases": read_quality.q30_bases,
            "q30Rate": read_quality.q30_rate,
            "gcContent": read_quality.gc_content
        }

        data['assemblyQuality'] = {
            "n50": assembly_quality.n50,
            "l50": assembly_quality.l50,
            "minContigLength": assembly_quality.minimum_contig_length,
            "numContigs": assembly_quality.num_contigs,
            "assemblySize": assembly_quality.length
        }

        # Heuristic (Species-based) Evaluation
        # Species Found:
        if species_evaluation.species_present:
            data['heuristicEvaluation'] = {
                "status": "evaluated",
                "evaluationMethod": "Species",
                "success": species_evaluation.success,
                "n50Pass": species_evaluation.n50_evaluation.success,
                "contigsPass": species_evaluation.contigs_evaluation.success,
                "l50Pass": species_evaluation.l50_evaluation.success,
                "lengthPass": species_evaluation.length_evaluation.success
            }

            # Thresholds
            data['heuristicEvaluation']['thresholds'] = {
                "numAssembliesForSpecies": database.get_count(species.name),
                "n50LowError": database.get_n50_quantile(species.name, database.LOW_ERROR_QUANTILE),
                "n50LowWarning": database.get_n50_quantile(species.name, database.LOW_WARNING_QUANTILE),
                "n50Median": database.get_n50_quantile(species.name, database.MEDIAN),
                "n50HighWarning": database.get_n50_quantile(species.name, database.HIGH_WARNING_QUANTILE),
                "n50HighError": database.get_n50_quantile(species.name, database.HIGH_ERROR_QUANTILE),
                "l50LowError": database.get_l50_quantile(species.name, database.LOW_ERROR_QUANTILE),
                "l50LowWarning": database.get_l50_quantile(species.name, database.LOW_WARNING_QUANTILE),
                "l50Median": database.get_l50_quantile(species.name, database.MEDIAN),
                "l50HighWarning": database.get_l50_quantile(species.name, database.HIGH_WARNING_QUANTILE),
                "l50HighError": database.get_l50_quantile(species.name, database.HIGH_ERROR_QUANTILE),
                "contigsLowError": database.get_contigs_quantile(species.name, database.LOW_ERROR_QUANTILE),
                "contigsLowWarning": database.get_contigs_quantile(species.name, database.LOW_WARNING_QUANTILE),
                "contigsMedian": database.get_contigs_quantile(species.name, database.MEDIAN),
                "contigsHighWarning": database.get_contigs_quantile(species.name, database.HIGH_WARNING_QUANTILE),
                "contigsHighError": database.get_contigs_quantile(species.name, database.HIGH_ERROR_QUANTILE),
                "lengthLowError": database.get_length_quantile(species.name, database.LOW_ERROR_QUANTILE),
                "lengthLowWarning": database.get_length_quantile(species.name, database.LOW_WARNING_QUANTILE),
                "lengthMedian": database.get_length_quantile(species.name, database.MEDIAN),
                "lengthHighWarning": database.get_length_quantile(species.name, database.HIGH_WARNING_QUANTILE),
                "lengthHighError": database.get_length_quantile(species.name, database.HIGH_ERROR_QUANTILE)
            }

        # Evaluation not performed:
        else:
            data['heuristicEvaluation'] = {
                "status": "not evaluated",
            }

        # Species information (always present):
        data['heuristicEvaluation']['speciesInDatabase'] = species_evaluation.species_present

        # NCBI Exclusion Evaluation
        data['NCBIFallbackEvaluation'] = {
            "status": "evaluated",
            "success": ncbi_evaluation.success,
            "n50Pass": ncbi_evaluation.n50_evaluation.success,
            "contigsPass": ncbi_evaluation.contigs_evaluation.success,
            "l50Pass": ncbi_evaluation.l50_evaluation.success,
            "lengthPass": ncbi_evaluation.length_evaluation.success
        }

        # Thresholds
        data['NCBIFallbackEvaluation']['thresholds'] = {
            "minLength": REFSEQ_MIN_LENGTH,
            "minN50": REFSEQ_MIN_N50,
            "maxL50": REFSEQ_MAX_L50,
            "maxContigs": REFSEQ_MAX_CONTIGS
        }

        # Machine learning-based evaluation:
        if machine_learning_evaluation.species_present:
            data['machineLearningEvaluation'] = {
                "status": "evaluated",
                "success": machine_learning_evaluation.success,
                "probability": machine_learning_evaluation.probability,
                "report": machine_learning_evaluation.report
            }
        # Machine learning evaluation not performed:
        else:
            data['machineLearningEvaluation'] = {
                "status": "not evaluated",
            }

        # Species information (always present):
        data['machineLearningEvaluation']['SpeciesInDatabase'] = machine_learning_evaluation.species_present

        with open(output_filename, 'w') as output_file:
            json.dump(data, output_file, indent=4)

        return output_filename
