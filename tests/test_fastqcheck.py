'''
Copyright:

University of Manitoba & National Microbiology Laboratory, Canada, 2020

Written by: Arnab Saha Mandal

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
'''

import os
from pathlib import Path

# Importing FastqCheck class from utilities.py
from proksee.utilities import FastqCheck

START_DIR = Path(__file__).parent.absolute()
TEST_INPUT_DIR = '{}/data/'.format(str(START_DIR))

# Valid fastq files for forward and reverse reads
forward_good = os.path.join(TEST_INPUT_DIR, 'genuine.fastq')
reverse_good = os.path.join(TEST_INPUT_DIR, 'SRR7947278_5pair_reads.fastq')

# Case 1: creating instance of class FastqCheck with valid read files
fastq_object_good = FastqCheck(forward_good, reverse_good)

'''
Creating lists of four possibilities of bad files
for forward and reverse reads
1. a fake fastq file
2. a non fastq text file
3. a non text readable file
4. a non existent file
'''

forward_bad = [
    os.path.join(TEST_INPUT_DIR, 'fake1.fastq'),
    os.path.join(TEST_INPUT_DIR, 'random1'),
    os.path.join(TEST_INPUT_DIR, 'winnipeg1.jpg'),
    os.path.join(TEST_INPUT_DIR, 'does_not_exist.fastq.gz')
]

reverse_bad = [
    os.path.join(TEST_INPUT_DIR, 'fake2.fastq'),
    os.path.join(TEST_INPUT_DIR, 'random2'),
    os.path.join(TEST_INPUT_DIR, 'winnipeg2.jpg'),
    os.path.join(TEST_INPUT_DIR, 'does_not_exist.fastq')
]

# Case 2-3: creating FastqCheck instances with one good and one bad read
fastq_object_good_fwd = FastqCheck(forward_good, reverse_bad[0])
fastq_object_good_rev = FastqCheck(forward_bad[0], reverse_good)

# Case 4-7: creating 4 FastqCheck instances with bad forward and reverse reads
fastq_object_bad = []
for i in range(0, 4):
    fastq_bad = FastqCheck(forward_bad[i], reverse_bad[i])
    fastq_object_bad.append(fastq_bad)

# Case 8: creating FastqCheck instance with forward only
fastq_object_rev_none = FastqCheck(forward_good, None)

# Running all tests for FastqCheck methods with different case instances


class TestFastqCheck():

    # Defining output variables for Case 1
    def case1_out(self):
        dicn_good = {forward_good: 1, reverse_good: 1}
        status_dicn_good = {forward_good: True, reverse_good: True}
        output_tuple_good = ('Read/s is/are valid fastq files..proceeding..', True)

        return (dicn_good, status_dicn_good, output_tuple_good)

    # Tests for Case 1: All tests with fastq_object_good
    def test_fastq_extn_check_good(self):
        method_extn_chk_good = fastq_object_good._FastqCheck__fastq_extn_check()
        assert self.case1_out()[0] == method_extn_chk_good

    def test_fastq_line_check_good(self):
        o1 = open(forward_good, 'r')
        o2 = open(reverse_good, 'r')
        method_o1 = fastq_object_good._FastqCheck__fastq_line_check(o1)
        method_o2 = fastq_object_good._FastqCheck__fastq_line_check(o2)
        assert method_o1
        assert method_o2

    def test_fastq_status_check_good(self):
        method_status_chk_good = fastq_object_good._FastqCheck__fastq_status(self.case1_out()[0])
        assert self.case1_out()[1] == method_status_chk_good

    def test_fastq_input_check_good(self):
        method_output_tuple_good = fastq_object_good.fastq_input_check()
        assert self.case1_out()[2] == method_output_tuple_good

    # Defining output variables for Case 2
    def case2_out(self):
        dicn_good_fwd = {forward_good: 1, reverse_bad[0]: 1}
        status_dicn_good_fwd = {forward_good: True, reverse_bad[0]: False}
        output_tuple_good_fwd = (
            'Either one or both of forward/reverse reads are invalid fastq files..exiting..',
            False
        )

        return (dicn_good_fwd, status_dicn_good_fwd, output_tuple_good_fwd)

    # Tests for Case 2: All tests with fastq_object_good_fwd
    def test_fastq_extn_check_good_fwd(self):
        method_extn_chk_good_fwd = fastq_object_good_fwd._FastqCheck__fastq_extn_check()
        assert self.case2_out()[0] == method_extn_chk_good_fwd

    def test_fastq_line_check_good_fwd(self):
        o1 = open(forward_good, 'r')
        o2 = open(reverse_bad[0], 'r')
        method_o1 = fastq_object_good_fwd._FastqCheck__fastq_line_check(o1)
        method_o2 = fastq_object_good_fwd._FastqCheck__fastq_line_check(o2)
        assert method_o1
        assert not method_o2

    def test_fastq_status_check_good_fwd(self):
        method_status_chk_good_fwd = fastq_object_good_fwd._FastqCheck__fastq_status(self.case2_out()[0])
        assert self.case2_out()[1] == method_status_chk_good_fwd

    def test_fastq_input_check_good_fwd(self):
        method_output_tuple = fastq_object_good_fwd.fastq_input_check()
        assert self.case2_out()[2] == method_output_tuple

    # Defining output variables for Case 3
    def case3_out(self):
        dicn_good_rev = {forward_bad[0]: 1, reverse_good: 1}
        status_dicn_good_rev = {forward_bad[0]: False, reverse_good: True}
        output_tuple_good_rev = (
            'Either one or both of forward/reverse reads are invalid fastq files..exiting..',
            False
        )

        return (dicn_good_rev, status_dicn_good_rev, output_tuple_good_rev)

    # Tests for Case 3: All tests with fastq_object_good_rev
    def test_fastq_extn_check_good_rev(self):
        method_extn_chk_good_rev = fastq_object_good_rev._FastqCheck__fastq_extn_check()
        assert self.case3_out()[0] == method_extn_chk_good_rev

    def test_fastq_line_check_good_rev(self):
        o1 = open(forward_bad[0], 'r')
        o2 = open(reverse_good, 'r')
        method_o1 = fastq_object_good_rev._FastqCheck__fastq_line_check(o1)
        method_o2 = fastq_object_good_rev._FastqCheck__fastq_line_check(o2)
        assert not method_o1
        assert method_o2

    def test_fastq_status_check_good_rev(self):
        method_status_chk_good_rev = fastq_object_good_rev._FastqCheck__fastq_status(self.case3_out()[0])
        assert self.case3_out()[1] == method_status_chk_good_rev

    def test_fastq_input_check_good_rev(self):
        method_output_tuple = fastq_object_good_rev.fastq_input_check()
        assert self.case3_out()[2] == method_output_tuple

    # Defining output variables for Case 4
    def case4_out(self):
        dicn_bad0 = {forward_bad[0]: 1, reverse_bad[0]: 1}
        status_dicn_bad0 = {forward_bad[0]: False, reverse_bad[0]: False}
        output_tuple_bad0 = ('Either one or both of forward/reverse reads are invalid fastq files..exiting..', False)

        return (dicn_bad0, status_dicn_bad0, output_tuple_bad0)

    # Tests for Case 4: All tests with fastq_object_bad[0]
    def test_fastq_extn_check_bad0(self):
        method_extn_chk_bad0 = fastq_object_bad[0]._FastqCheck__fastq_extn_check()
        assert self.case4_out()[0] == method_extn_chk_bad0

    def test_fastq_line_check_bad0(self):
        o1 = open(forward_bad[0], 'r')
        o2 = open(reverse_bad[0], 'r')
        method_o1 = fastq_object_bad[0]._FastqCheck__fastq_line_check(o1)
        method_o2 = fastq_object_bad[0]._FastqCheck__fastq_line_check(o2)
        assert not method_o1
        assert not method_o2

    def test_fastq_status_check_bad0(self):
        method_status_chk_bad0 = fastq_object_bad[0]._FastqCheck__fastq_status(self.case4_out()[0])
        assert self.case4_out()[1] == method_status_chk_bad0

    def test_fastq_input_check_bad0(self):
        method_output_tuple = fastq_object_bad[0].fastq_input_check()
        assert self.case4_out()[2] == method_output_tuple

    # Defining output variables for Case 5
    def case5_out(self):
        dicn_bad1 = {forward_bad[1]: 2, reverse_bad[1]: 2}
        status_dicn_bad1 = {forward_bad[1]: False, reverse_bad[1]: False}
        output_tuple_bad1 = ('Either one or both of forward/reverse reads are invalid fastq files..exiting..', False)

        return (dicn_bad1, status_dicn_bad1, output_tuple_bad1)

    # Tests for Case 5: All tests with fastq_object_bad[1]
    def test_fastq_extn_check_bad1(self):
        method_extn_chk_bad1 = fastq_object_bad[1]._FastqCheck__fastq_extn_check()
        assert self.case5_out()[0] == method_extn_chk_bad1

    def test_fastq_line_check_bad1(self):
        o1 = open(forward_bad[1], 'r')
        o2 = open(reverse_bad[1], 'r')
        method_o1 = fastq_object_bad[1]._FastqCheck__fastq_line_check(o1)
        method_o2 = fastq_object_bad[1]._FastqCheck__fastq_line_check(o2)
        assert not method_o1
        assert not method_o2

    def test_fastq_status_check_bad1(self):
        method_status_chk_bad1 = fastq_object_bad[1]._FastqCheck__fastq_status(self.case5_out()[0])
        assert self.case5_out()[1] == method_status_chk_bad1

    def test_fastq_input_check_bad1(self):
        method_output_tuple = fastq_object_bad[1].fastq_input_check()
        assert self.case5_out()[2] == method_output_tuple

    # Defining output variables for Case 6
    def case6_out(self):
        dicn_bad2 = {forward_bad[2]: 2, reverse_bad[2]: 2}
        status_dicn_bad2 = {forward_bad[2]: False, reverse_bad[2]: False}
        output_tuple_bad2 = ('Either one or both of forward/reverse reads are invalid fastq files..exiting..', False)

        return (dicn_bad2, status_dicn_bad2, output_tuple_bad2)

    # Tests for Case 6: All tests with fastq_object_bad[2]
    def test_fastq_extn_check_bad2(self):
        method_extn_chk_bad2 = fastq_object_bad[2]._FastqCheck__fastq_extn_check()
        assert self.case6_out()[0] == method_extn_chk_bad2

    def test_fastq_line_check_bad2(self):
        o1 = open(forward_bad[2], 'r')
        o2 = open(reverse_bad[2], 'r')
        method_o1 = fastq_object_bad[2]._FastqCheck__fastq_line_check(o1)
        method_o2 = fastq_object_bad[2]._FastqCheck__fastq_line_check(o2)
        assert not method_o1
        assert not method_o2

    def test_fastq_status_check_bad2(self):
        method_status_chk_bad2 = fastq_object_bad[2]._FastqCheck__fastq_status(self.case6_out()[0])
        assert self.case6_out()[1] == method_status_chk_bad2

    def test_fastq_input_check_bad2(self):
        method_output_tuple = fastq_object_bad[2].fastq_input_check()
        assert self.case6_out()[2] == method_output_tuple

    # Defining output variables for Case 7
    def case7_out(self):
        dicn_bad3 = {forward_bad[3]: 0, reverse_bad[3]: 1}
        status_dicn_bad3 = {forward_bad[3]: False, reverse_bad[3]: False}
        output_tuple_bad3 = ('Either one or both of forward/reverse reads are invalid fastq files..exiting..', False)

        return (dicn_bad3, status_dicn_bad3, output_tuple_bad3)

    # Tests for Case 7: All tests with fastq_object_bad[3]
    def test_fastq_extn_check_bad3(self):
        method_extn_chk_bad3 = fastq_object_bad[3]._FastqCheck__fastq_extn_check()
        assert self.case7_out()[0] == method_extn_chk_bad3

    def test_fastq_status_check_bad3(self):
        method_status_chk_bad3 = fastq_object_bad[3]._FastqCheck__fastq_status(self.case7_out()[0])
        assert self.case7_out()[1] == method_status_chk_bad3

    '''The output of __fastq_status is from FileNotFoundError exception.
    Hence test for __fast_line_check method is not applicable'''

    def test_fastq_input_check_bad3(self):
        method_output_tuple = fastq_object_bad[3].fastq_input_check()
        assert self.case7_out()[2] == method_output_tuple

    # Defining output variables for Case 8
    def case8_out(self):
        dicn_revnone = {forward_good: 1}
        status_dicn_revnone = {forward_good: True}
        output_tuple_revnone = ('Read/s is/are valid fastq files..proceeding..', True)

        return (dicn_revnone, status_dicn_revnone, output_tuple_revnone)

    # Tests for Case 8: All tests with fastq_object_rev_none
    def test_fastq_extn_check_revnone(self):
        method_extn_chk = fastq_object_rev_none._FastqCheck__fastq_extn_check()
        assert self.case8_out()[0] == method_extn_chk

    def test_fastq_line_check_revnone(self):
        o1 = open(forward_good, 'r')
        method_o1 = fastq_object_rev_none._FastqCheck__fastq_line_check(o1)
        assert method_o1

    def test_fastq_status_check_revnone(self):
        method_status_chk = fastq_object_rev_none._FastqCheck__fastq_status(self.case8_out()[0])
        assert self.case8_out()[1] == method_status_chk

    def test_fastq_input_check_revnone(self):
        method_output_tuple = fastq_object_rev_none.fastq_input_check()
        assert self.case8_out()[2] == method_output_tuple
