import re
import gzip
import sys
import os

GZ_TRUE = 0
GZ_FALSE = 1


class FastqCheck():


    def __init__(self, forward, reverse):
        self.forward = forward
        self.reverse = reverse


    def fastq_extn_check(self, forward, reverse):
        if reverse is None:
            file_list = [forward]
        else:
            file_list = [forward, reverse]
        f_name_dicn = {}
        fastq_ext = ['fastq', 'fq']
        for f_name in file_list:
            array_f = f_name.split('.')
            try:
                if (array_f[-2] in fastq_ext and array_f[-1] == 'gz'):
                    f_name_dicn[f_name] = GZ_TRUE
                elif (array_f[-1] in fastq_ext):
                    f_name_dicn[f_name] = GZ_FALSE
            except IndexError:
                pass
        
        return f_name_dicn


    def fastq_status(self, f_name_dicn):
        status = {}
        for file in f_name_dicn:
            if (f_name_dicn[file] == GZ_TRUE):
                with gzip.open(file, mode='rt') as open_file:
                    status[file] = self.fastq_line_check(open_file)
            elif (f_name_dicn[file] == GZ_FALSE):
                with open(file, mode='r') as open_file:
                    status[file] = self.fastq_line_check(open_file)
        return status

    def fastq_line_check(self, open_file):
        count_line = 0
        fastq_attr = {}; fastq = {}
        fastq_attr[open_file] = 0
        for line in open_file:
            count_line += 1

            if count_line == 1:
                one = re.match(r'^@.+', line)
                if one is not None:
                    fastq_attr[open_file] += 1

            elif count_line == 2:
                two = re.match(r'^[ATGCN]+$', line)
                if two is not None:
                    fastq_attr[open_file] += 1

            elif count_line == 3:
                three = re.match(r'^\+.*', line)
                if three is not None:
                    fastq_attr[open_file] += 1

            elif count_line == 4:
                four = re.match(r'.+', line)
                if four is not None:
                    fastq_attr[open_file] += 1

                break

        if fastq_attr[open_file] == 4:
            fastq[open_file] = True
        else:
            fastq[open_file] = False

        return fastq[open_file]


    def fastq_input_check(self, forward, reverse):
        extn_dicn = self.fastq_extn_check(forward, reverse)
        status_dicn = self.fastq_status(extn_dicn)
        if status_dicn[forward] or status_dicn[reverse]:
            output_string = 'Read/s are valid fastq file/s..proceeding..'
            status = True
        elif not status_dicn[forward] and not status_dicn[reverse]:
            output_string = 'Read/s are invalid fastq file/s..exiting..'
            status = False

        return (output_string, status)