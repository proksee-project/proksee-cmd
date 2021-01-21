'''
Copyright:

University of Manitoba & National Microbiology Laboratory, Canada, 2020

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
'''

import gzip
import re

from enum import Enum
from proksee.input_verification import is_gzipped


class Platform(Enum):
    UNIDENTIFIABLE = "Unidentifiable"
    ILLUMINA = "Illumina"
    ION_TORRENT = "Ion Torrent"
    PAC_BIO = "Pac Bio"


def identify_reads(reads):

    if is_gzipped(reads):
        open_file = gzip.open(reads, mode='rt')

    else:
        open_file = open(reads, mode='r')

    first_line = open_file.readline()
    first_line = first_line.rstrip('\n')

    '''Separating first line characters based on patterns'''
    chars_ill = first_line.split(':')
    chars_pac = first_line.split('/')

    '''Assigning sequencing platform/s based on first line patterns'''
    if len(chars_ill) == 3:
        platform = Platform.ION_TORRENT

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
                platform = Platform.ILLUMINA
            else:
                platform = Platform.UNIDENTIFIABLE

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
                platform = Platform.ILLUMINA
            else:
                platform = Platform.UNIDENTIFIABLE

        else:
            platform = Platform.UNIDENTIFIABLE

    elif len(chars_pac) > 2:
        platform = Platform.PAC_BIO

    else:
        platform = Platform.UNIDENTIFIABLE

    open_file.close()

    return platform


def identify_name(platform_name):
    """
    Identifies the sequencing platform based on the passed name of the platform.

    PARAMETERS:
        platform_name (string): the name of the platform

    RETURNS:
        platform (Platform): the sequencing platform
    """

    if platform_name.lower() == Platform.ILLUMINA.value.lower():
        platform = Platform.ILLUMINA

    elif platform_name.lower() == Platform.PAC_BIO.value.lower():
        platform = Platform.PAC_BIO

    elif platform_name.lower() == Platform.ION_TORRENT.value.lower():
        platform = Platform.ION_TORRENT

    else:
        platform = Platform.UNIDENTIFIABLE

    return platform


class PlatformIdentifier():

    def __init__(self, reads):
        """
        Initializes the (sequencing) Platform Identifier.

        PARAMETERS
            reads (Reads): the reads for which to identify the sequencing platform
        """

        self.reads = reads

    def identify(self):
        """
        Identifies the sequencing platform.

        RETURNS
            platform (Platform): the identified platform as an Enum member value
        """

        forward_platform = identify_reads(self.reads.forward)
        platform = forward_platform

        # Check that the reverse reads have the same platform:
        if self.reads.reverse:
            reverse_platform = identify_reads(self.reads.reverse)

            if forward_platform != reverse_platform:
                platform = Platform.UNIDENTIFIABLE

        return platform
