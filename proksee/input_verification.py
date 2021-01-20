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

import gzip
import os
import re


def has_valid_fastq_extension(file_location):
    """
    Determines whether or not the passed file location has a valid FASTQ or GZIP'd FASTQ file extension.

    ARGUMENTS
        file_location (str): the location of the file to check

    RETURNS
        valid (bool): whether or not the file location has a valid FASTQ extension
    """

    valid_extensions = ("fastq", "fq", "fastq.gz", "fq.gz")
    valid = file_location.lower().endswith(valid_extensions)  # Case insensitive matching

    return valid


def has_valid_fastq_encoding(file):
    """
    Determines whether or not the passed file appears to be encoded as a FASTQ file.

    ARGUMENTS
        file (File): an open and readable file

    RETURNS
        valid (bool): whether or not the file is encoded as a FASTQ file
    """

    # First line starts with '@' and has at least one other character following:
    line = file.readline()
    if not (len(line) > 0 and re.match(r'^@.+', line)):
        return False

    # Second line contains one or more A, C, G, T, and N characters:
    sequence = file.readline()
    if not (len(sequence) > 0 and re.match(r'^[ATGCN]+$', sequence)):
        return False

    # Third line begins with '+' and has any number of optional characters following:
    line = file.readline()
    if not (len(line) > 0 and re.match(r'^\+.*', line)):
        return False

    # Fourth line contains sequencing encoding characters:
    encoding = file.readline()
    if not (len(encoding) > 0 and re.match(r'^\S+$', encoding)):
        return False

    # The length of the sequence and encoding must be the same:
    if not (len(sequence) == len(encoding)):
        return False

    return True


def is_valid_fastq(file_location):
    """
    Determines whether or not the passed file location appears to be a valid FASTQ-formatted file.

    ARGUMENTS
        file_location (str): the location of the file to check

    RETURNS
        valid (bool): whether or not the passed file appears to be a valid FASTQ-formatted file
    """

    if not os.path.isfile(file_location):
        return False

    if not has_valid_fastq_extension(file_location):
        return False

    if is_gzipped(file_location):
        file = gzip.open(file_location, mode='rt')

    else:
        file = open(file_location, mode='r')

    valid = has_valid_fastq_encoding(file)
    file.close()

    return valid


def are_valid_fastq(reads):
    """
    Determines whether or not the passed reads appear to be valid FASTQ-formatted files.

    ARGUMENTS
        reads (Reads): the reads to check

    RETURNS
        valid (bool): whether or not the reads appear to be FASTQ-formatted
    """

    for file_location in reads.get_file_locations():
        if not is_valid_fastq(file_location):
            return False

    return True


def is_gzipped(file_location):
    """
    Determines whether or not the passed file appears to be in GZIP format.

    ARGUMENTS
        file_location (str): the location of the file to check

    RETURNS
        gzipped (bool): whether or not the file appears to be in GZIP format
    """

    GZIP = ".gz"

    if file_location.endswith(GZIP):
        gzipped = True
    else:
        gzipped = False

    return gzipped
