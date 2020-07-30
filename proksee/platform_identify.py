import os
import gzip
import sys

# Declaring global variables based on zipped or unzipped files
GZ_FALSE = 0
GZ_TRUE = 1


# Checking files for valid fastq extension, passing to dictionary
def fastq_extn_check(fwd=None, rev=None):
    if rev == 'use_pair':
        file_list = [fwd]
    else:
        file_list = [fwd, rev]

    f_name_dicn = {}
    fastq_ext = ['fastq', 'fq']
    for f_name in file_list:
        
        '''splitting file names by . to capture extension'''
        array_f = f_name.split('.')
        try:
            
            '''Checking for zipped fastq file. Append file name
            and value to dictionary'''
            if (array_f[-2] in fastq_ext and array_f[-1] == 'gz'):
                f_name_dicn[f_name] = GZ_TRUE
            
                '''Checking for unzipped fastq file. Append file name
                and value to dictionary'''
            elif (array_f[-1] in fastq_ext):
                f_name_dicn[f_name] = GZ_FALSE

            '''Raising exception if no fastq files exist'''
        except IndexError:
            pass

    return f_name_dicn

# Identifying sequencing platform based on read
def plat_iden(open_file=None):
    
    '''Initinalizing line counting for a file'''
    count_line = 0

    '''Grabbing the first line only'''
    for line in open_file:
        count_line += 1
        if count_line == 1:
            first_line = line.rstrip('\n')
            break
    
    '''Investigating contents of first line'''
    chars_ill = first_line.split(':')
    chars_pac = first_line.split('/')

    if len(chars_ill) == 3:
        platform = 'Ion Torrent'

    elif len(chars_ill) > 4:
        platform = 'Illumina'

    elif len(chars_pac) > 2:
        platform = 'Pacbio'

    else:
        platform = 'Unidentifiable'

    return platform


# Opening files within input directory and assigning plat_iden method
def platform_output(f_name_dicn=None):
    
    '''Writing file and platform names in dictionary'''
    fastq_platform = {}

    '''Iterating through input file dictionary'''
    for file in f_name_dicn:

        '''Almost identical operations for zipped/unzipped files'''
        if (f_name_dicn[file] == GZ_TRUE):
            with gzip.open(file, mode='rt') as open_file:
                fastq_platform[file] = plat_iden(open_file)


        elif (f_name_dicn[file] == GZ_FALSE):
            with open(file, mode='r') as open_file:
                fastq_platform[file] = plat_iden(open_file)

    return fastq_platform

def main():
    '''Initiating main function with mandatory parameters = 2'''
    if len(sys.argv) != 3:
        sys.exit('''
        Command usage: python platform_identification.py FORWARD_READ REVERSE_READ.
        Need to pass 2 arguments for forward and reverse fastq reads.
        For single read, use "use_pair" as an argument in lieu of reverse read.
        ''')
    
    forward_read = sys.argv[1]
    reverse_read = sys.argv[2]

    '''Creating dictionary of file names and zipped/unzippped status'''
    file_dicn = fastq_extn_check(forward_read, reverse_read)
    
    '''Output dictionary of file names and possible sequencing platform'''
    output_dicn = platform_output(file_dicn)
    for key, value in output_dicn.items():
        sys.stdout.write(key + ': ' + value + '\n')


if __name__ == '__main__':
    main()