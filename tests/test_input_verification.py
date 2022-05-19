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
from proksee.input_verification import is_gzipped, is_valid_fastq, has_valid_fastq_extension, are_valid_fastq
from proksee.reads.reads import Reads


class TestInputVerification:

    def test_has_valid_fastq_extension_true(self):
        """
        Tests when the file appears to have a good extension.
        """

        assert has_valid_fastq_extension("reads.fq")
        assert has_valid_fastq_extension("reads.fastq")
        assert has_valid_fastq_extension("reads.fq.gz")
        assert has_valid_fastq_extension("reads.fastq.gz")

    def test_has_valid_fastq_extension_false(self):
        """
        Tests when the file appears to have a bad extension.
        """

        assert not has_valid_fastq_extension("reads.fa")
        assert not has_valid_fastq_extension("reads.fasta")
        assert not has_valid_fastq_extension("reads.fa.gz")
        assert not has_valid_fastq_extension("reads.fasta.gz")
        assert not has_valid_fastq_extension("reads.fq.zip")
        assert not has_valid_fastq_extension("reads.fastq.zip")
        assert not has_valid_fastq_extension("reads.fq.fa")
        assert not has_valid_fastq_extension("reads.fasq")

    def test_is_valid_fastq_true(self):
        """
        Tests when the FASTQ file is valid.
        """

        fastq_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "genuine.fastq")
        valid = is_valid_fastq(fastq_location)

        assert valid

    def test_is_valid_fastq_true_gzip(self):
        """
        Tests when the FASTQ file is valid when gzipped.
        """

        fastq_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "genuine.fastq.gz")
        valid = is_valid_fastq(fastq_location)

        assert valid

    def test_is_valid_fastq_missing_file(self):
        """
        Tests when the FASTQ file is missing.
        """

        fastq_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "missing_file.fastq")
        valid = is_valid_fastq(fastq_location)

        assert not valid

    def test_is_valid_fastq_wrong_filetype(self):
        """
        Tests when the file appears to have the wrong extension.
        """

        fastq_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "simple_contig.fasta")
        valid = is_valid_fastq(fastq_location)

        assert not valid

    def test_is_valid_fastq_bad_header(self):
        """
        Tests when the FASTQ file has a bad FASTQ header (line 1 of 4).
        """

        fastq_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "fake1.fastq")
        valid = is_valid_fastq(fastq_location)

        assert not valid

    def test_is_valid_fastq_bad_nucleotides(self):
        """
        Tests when the FASTQ file has a bad nucleotides encoding (line 2 of 4).
        """

        fastq_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "fake2.fastq")
        valid = is_valid_fastq(fastq_location)

        assert not valid

    def test_bad_fastq_third_line(self):
        """
        Tests when the third line of the FASTQ file is wrong (not a "+").
        """

        fastq_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "bad_format1.fastq")
        valid = is_valid_fastq(fastq_location)

        assert not valid

    def test_bad_fastq_quality_encoding(self):
        """
        Tests when the encoding of the quality scores of the FASTQ file are wrong.
        """

        fastq_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "bad_format2.fastq")
        valid = is_valid_fastq(fastq_location)

        assert not valid

    def test_bad_fastq_quality_length(self):
        """
        Tests when the length of the quality scores of the FASTQ file are wrong.
        """

        fastq_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "bad_format3.fastq")
        valid = is_valid_fastq(fastq_location)

        assert not valid

    def test_reads_valid_fastq_true(self):
        """
        Tests when reads refer to valid FASTQ file(s).
        """

        fastq_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "genuine.fastq")
        reads = Reads(fastq_location, None)
        valid = are_valid_fastq(reads)

        assert valid

    def test_reads_valid_fastq_false(self):
        """
        Tests when reads refer to invalid FASTQ file(s).
        """

        fastq_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "simple_contig.fasta")
        reads = Reads(fastq_location, None)
        valid = are_valid_fastq(reads)

        assert not valid

    def test_is_gzipped_true(self):
        """
        Tests when the file extension is ".gz".
        """

        file_location = "myfile.gz"
        gzipped = is_gzipped(file_location)

        assert gzipped

    def test_is_gzipped_false(self):
        """
        Tests when the file extension is NOT ".gz".
        """

        file_location = "myfile.gbk"
        gzipped = is_gzipped(file_location)

        assert not gzipped
