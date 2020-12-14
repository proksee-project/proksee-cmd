import re
import gzip

# Declaring global variables based on zipped, unzipped fastq files
# and other possibilities
GZ_TRUE = 0
GZ_FALSE = 1
INVALID = 2


# Defining class for checking fastq files
class FastqCheck():

    # Defining __init__ method with reads parameters
    def __init__(self, forward, reverse):
        self.forward = forward
        self.reverse = reverse

    # Method for creating dictionary based on fastq filenames
    def __fastq_extn_check(self):
        '''Creating file list based on forward and/or reverse reads'''
        if self.reverse is None:
            file_list = [self.forward]
        else:
            file_list = [self.forward, self.reverse]

        '''Initializing file name dictionary'''
        f_name_dicn = {}

        '''Listing possible fastq extension names'''
        fastq_ext = ['fastq', 'fq']

        '''Iterating through file list, identifying extension names'''
        for f_name in file_list:
            array_f = f_name.split('.')

            try:
                '''For zipped fastq file'''
                if (array_f[-2] in fastq_ext and array_f[-1] == 'gz'):
                    f_name_dicn[f_name] = GZ_TRUE

                    '''For unzipped fastq file'''
                elif (array_f[-1] in fastq_ext):
                    f_name_dicn[f_name] = GZ_FALSE

                    '''For invalid files without fastq extension'''
                else:
                    f_name_dicn[f_name] = INVALID

                '''For invalid files without any dot extension'''
            except IndexError:
                f_name_dicn[f_name] = INVALID

        return f_name_dicn

    # Method for assigning boolean status to fastq files, outputting dictionary
    def __fastq_status(self, f_name_dicn):
        status = {}

        '''Iterating though file name: extension dictionary'''
        for file in f_name_dicn:

            '''Zipped/unzipped files examined by __fastq_line_check method for truth.
            Non existent files are caught by exception and labelled false'''
            if (f_name_dicn[file] == GZ_TRUE):
                try:
                    with gzip.open(file, mode='rt') as open_file:
                        status[file] = self.__fastq_line_check(open_file)
                except FileNotFoundError:
                    status[file] = False

            else:
                try:
                    with open(file, mode='r') as open_file:
                        status[file] = self.__fastq_line_check(open_file)
                except FileNotFoundError:
                    status[file] = False

                '''Returning dictionary of file names: fastq boolean status'''
        return status

    # Method for line by line (upto 4) evatulation of fastq file
    # Specifying filehandle as a parameter
    def __fastq_line_check(self, open_file):
        '''Initializing line counts and fastq attributes count'''
        count_line = 0
        fastq_attr_count = 0

        '''Incrementing line counts and fastq attributes counts. The latter
        evaluated by separate regular expressions for each line'''
        try:
            for line in open_file:
                count_line += 1

                if count_line == 1:
                    one = re.match(r'^@.+', line)

                    '''First line of fastq begins with @'''
                    if one is not None:
                        fastq_attr_count += 1

                elif count_line == 2:
                    two = re.match(r'^[ATGCN]+$', line)

                    '''Second line of fastq contains DNA sequence. Its length captured for
                    comparison with line 4'''
                    if two is not None:
                        fastq_attr_count += 1
                        len_two = len(line.rstrip('\n'))

                elif count_line == 3:
                    three = re.match(r'^\+.*', line)

                    '''Third line begins with + followed by optional'''
                    if three is not None:
                        fastq_attr_count += 1

                elif count_line == 4:
                    four = re.match(r'^\S+$', line)

                    '''Fourth line has ASCII characters for sequence quality.
                    Number of characters should be the same as second line'''
                    if four is not None:
                        len_four = len(line.rstrip('\n'))
                        try:
                            if len_four == len_two:
                                fastq_attr_count += 1

                            '''For text readable but invalid fastq files len_two will not hold'''
                        except UnboundLocalError:
                            pass

                            '''Exiting line wise reading after 4 lines'''
                    break

            '''Summarizing fastq attribute count and assigning boolean'''
            if fastq_attr_count == 4:
                return True
            else:
                return False

            '''If files are not ASCII readable (e.g. image, mandarin etc.)'''
        except UnicodeDecodeError:
            return False

    # Method for integrating private functions
    def fastq_input_check(self):
        extn_dicn = self.__fastq_extn_check()
        status_dicn = self.__fastq_status(extn_dicn)

        '''Defining output string and setting boolean to True'''
        status = True

        '''boolean is false if either conditions are not met
        1. forward status is False
        2. reverse is specified and reverse status is False'''
        if (not status_dicn[self.forward] or self.reverse is not None and not status_dicn[self.reverse]):
            status = False

        return status
