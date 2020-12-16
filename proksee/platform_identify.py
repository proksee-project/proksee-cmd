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

import gzip
from proksee.utilities import FastqCheck
import re

# Declaring global variables based on zipped or unzipped files
GZ_TRUE = 0
GZ_FALSE = 1


# Defining class for identifying sequencing platform
class PlatformIdentifier():

    # Defining __init__ method with reads parameters
    def __init__(self, forward, reverse):
        self.forward = forward
        self.reverse = reverse

    # Method for identifying sequencing platform based on read
    '''Passing file handle as a parameter'''
    def __plat_iden(self, open_file):
        count_line = 0

        '''Extracting the first line of fastq file, terminating'''
        for line in open_file:
            count_line += 1
            if count_line == 1:
                first_line = line.rstrip('\n')
                break

        '''Separating first line characters based on patterns'''
        chars_ill = first_line.split(':')
        chars_pac = first_line.split('/')

        '''Assigning sequencing platform/s based on first line patterns'''
        if len(chars_ill) == 3:
            platform = 'Ion Torrent'

        elif len(chars_ill) > 4:
            '''Recent illumina fastq have the format
            @<instrument>:<run number>:<flowcell ID>:<lane>:<tile>:<xpos>:<y-pos>
            <read>:<is filtered>:<control number>:<index>'''
            if len(chars_ill) == 10:
                illumina_attr = 0

                instrument_num = re.match(r'^@[a-zA-Z0-9_]+$', chars_ill[0])
                if instrument_num is not None:
                    illumina_attr += 1

                run = re.match(r'^\d+$', chars_ill[1])
                if run is not None:
                    illumina_attr += 1

                flowcell_id = re.match(r'^[a-zA-Z0-9]+$', chars_ill[2])
                if flowcell_id is not None:
                    illumina_attr += 1

                for n in range(3, 6):
                    lane_to_xpos = re.match(r'^\d+$', chars_ill[n])
                    if lane_to_xpos is not None:
                        illumina_attr += 1

                filtered = re.match(r'^[YN]$', chars_ill[7])
                if filtered is not None:
                    illumina_attr += 1

                control_num = re.match(r'^\d+$', chars_ill[8])
                if control_num is not None:
                    illumina_attr += 1

                if illumina_attr == 8:
                    platform = 'Illumina'
                else:
                    platform = 'Unidentifiable'

                '''Older illumina fastq have the format
                @<machine_id>:<lane>:<tile>:<x_coord>:<y_coord>#<index>/<read>'''
            elif len(chars_ill) == 5:
                illumina_attr = 0

                machine_id = re.match(r'^@[a-zA-Z0-9_]+$', chars_ill[0])
                if machine_id is not None:
                    illumina_attr += 1

                for n in range(1, 4):
                    lane_to_xpos = re.match(r'^\d+$', chars_ill[n])
                    if lane_to_xpos is not None:
                        illumina_attr += 1

                if illumina_attr == 4:
                    platform = 'Illumina'
                else:
                    platform = 'Unidentifiable'

            else:
                platform = 'Unidentifiable'

        elif len(chars_pac) > 2:
            platform = 'Pacbio'

        else:
            platform = 'Unidentifiable'

        return platform

    # Opening files within input file dictionary and assigning plat_iden method
    def __platform_output(self, f_name_dicn):
        platform_dicn = {}

        '''Iterating through input file dictionary'''
        for file in f_name_dicn:

            '''Separate opening functions for zipped/unzipped files'''
            if (f_name_dicn[file] == GZ_TRUE):
                with gzip.open(file, mode='rt') as open_file:
                    platform_dicn[file] = self.__plat_iden(open_file)

            elif (f_name_dicn[file] == GZ_FALSE):
                with open(file, mode='r') as open_file:
                    platform_dicn[file] = self.__plat_iden(open_file)

            '''Returning file:platform as key:value in dictionary'''
        return platform_dicn

    # Method for integrating private functions
    def identify(self):
        '''Creating instance of FastqCheck class'''
        fastq_object = FastqCheck(self.forward, self.reverse)

        '''Creating input file dictionary from private method of FastqCheck'''
        f_name_dicn = fastq_object._FastqCheck__fastq_extn_check()

        '''Creating platform dictionary for input file dictionary'''
        platform_dicn = self.__platform_output(f_name_dicn)

        '''Creating output string for forward only if reverse is None'''
        if self.reverse is None:
            output_string = str(platform_dicn[self.forward])

            '''Checking conditions if reverse is specified'''
        else:

            '''Creating output string if forward and reverse platforms are same'''
            if platform_dicn[self.forward] == platform_dicn[self.reverse]:
                output_string = str(platform_dicn[self.forward])

                '''Creating output string if forward and reverse platforms are different'''
            else:
                output_string1 = str(platform_dicn[self.forward])
                output_string2 = str(platform_dicn[self.reverse])
                output_string = output_string1 + "/" + output_string2

        return output_string
