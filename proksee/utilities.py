import re
import gzip
import sys
import os
from collections import defaultdict


GZ_TRUE = 0
GZ_FALSE = 1
INVALID = 2

class FastqCheck():


    def __init__(self, forward, reverse):
        self.forward = forward
        self.reverse = reverse


    def __fastq_extn_check(self):
        if self.reverse is None:
            file_list = [self.forward]
        else:
            file_list = [self.forward, self.reverse]
        f_name_dicn = {}
        fastq_ext = ['fastq', 'fq']
        for f_name in file_list:
            array_f = f_name.split('.')
            
            try:
                if (array_f[-2] in fastq_ext and array_f[-1] == 'gz'):
                    f_name_dicn[f_name] = GZ_TRUE
                
                elif (array_f[-1] in fastq_ext):
                    f_name_dicn[f_name] = GZ_FALSE
                
                else:
                    '''For invalid files without fastq extension'''
                    f_name_dicn[f_name] = INVALID
                
                '''For invalid files without any extension'''
            
            except IndexError:
                f_name_dicn[f_name] = INVALID

        return f_name_dicn


    def __fastq_status(self, f_name_dicn):
        status = {}
        for file in f_name_dicn:
            
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

        return status


    def __fastq_line_check(self, open_file):
        count_line = 0
        fastq_attr_count = 0
        try:
            for line in open_file:
                count_line += 1

                if count_line == 1:
                    one = re.match(r'^@.+', line)
                    if one is not None:
                        fastq_attr_count += 1

                elif count_line == 2:
                    two = re.match(r'^[ATGCN]+$', line)
                    if two is not None:
                        fastq_attr_count += 1
                        len_two = len(line.rstrip('\n'))

                elif count_line == 3:
                    three = re.match(r'^\+.*', line)
                    if three is not None:
                        fastq_attr_count += 1

                elif count_line == 4:
                    four = re.match(r'^\S+$', line)
                    if four is not None:
                        len_four = len(line.rstrip('\n'))
                        try:
                            if len_four == len_two:
                                fastq_attr_count += 1

                            '''For text readable but invalid fastq files, 
                            regex at second line of file will not hold'''
                        except UnboundLocalError:
                            pass

                    break

            if fastq_attr_count == 4:
                return True
            else:
                return False

            '''For non ASCII input files'''
        except UnicodeDecodeError:
            return False


    def fastq_input_check(self):
        extn_dicn = self.__fastq_extn_check()
        status_dicn = self.__fastq_status(extn_dicn)

        output_string = 'Read/s is/are valid fastq files..proceeding..'
        status = True

        if not status_dicn[self.forward] or \
            self.reverse is not None and not status_dicn[self.reverse]:
                output_string = 'Either one or both of forward/reverse reads are invalid fastq files..exiting..'
                status = False

        return (output_string, status)