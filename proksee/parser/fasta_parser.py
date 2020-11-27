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


def split_multi_fasta_into_fasta(fasta_file, output_directory):
    """
    Splits a single multi-FASTA-format file into individual FASTA-format files, each containing only one FASTA record.

    PARAMETERS
        fasta_file (str): the file location of the FASTA file
        output_directory (str): the output directory to place all of the individual FASTA files

    RETURNS
        file_list (list(str)): a list of the locations of the written FASTA files in descending order of sequence length

    POST
        The output directory will contain a number of FASTA files equal to the number of FASTA records in the
        multi-FASTA-format file provided to this function.
    """

    count = 0
    file_list = []

    if not os.path.exists(fasta_file):
        raise FileNotFoundError("File not found: " + fasta_file)

    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    with open(fasta_file) as file:

        for line in file:
            # FASTA record header
            if line.startswith(">"):
                output_file = os.path.join(output_directory, str(count) + ".fasta")
                output = open(output_file, "w")
                count += 1

                information = [output_file, 0]  # [filename, number of sequence characters]
                file_list.append(information)

                output.write(line)

            # FASTA record sequence
            else:
                output.write(line)
                file_list[len(file_list) - 1][1] += len(line)  # last item in list, increment sequence characters

    file_list.sort(key=lambda filename: filename[1], reverse=True)

    # Keep only filenames (not number of characters)
    for i in range(len(file_list)):
        file_list[i] = file_list[i][0]

    return file_list
