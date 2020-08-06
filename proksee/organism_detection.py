import os
import sys
import subprocess, shlex
import pandas as pd
from collections import defaultdict
import operator


def refseq_masher_string(fwd=None,rev=None):
    if rev is None:
        ref_str = 'refseq_masher matches ' + fwd
    elif rev.endswith('fastq') or rev.endswith('fq'):
        ref_str = 'refseq_masher matches ' + fwd + ' ' + rev
    
    return ref_str


def refseq_masher_func(ref_str=None, output_dir=None):
    refseq_out = os.path.join(output_dir, 'refseq.out')
    refseq_log = os.path.join(output_dir, 'refseq.log')
    stdout = open(refseq_out, 'w+')
    stderr = open(refseq_log, 'w+')
    try:
        subprocess.call(ref_str, shell=True, stdout=stdout, stderr=stderr)
    except subprocess.CalledProcessError as e:
        raise e
    
    return refseq_out


def identify_organism(refseq_out=None, output_dir=None):
    '''Initiating counting of output organisms'''
    organism_counter = defaultdict(int)

    '''Opening refseq_masher output file'''
    with open(refseq_out, 'r') as open_file:
        for line in open_file:

            '''Leaving out blank lines and isolating 2nd column'''
            if len(line.strip()) > 0:
                col2 = line.split('\t')[1]
                
                try:
                    '''Joining genus and species name, counting occurrences'''
                    test_organism = col2.split(' ')[0] + ' ' + col2.split(' ')[1]
                    organism_counter[test_organism] += 1

                except Exception:
                    pass
    
    try:
        '''Output organism with highest number of occurrences'''
        major_org = max(organism_counter.items(), key=operator.itemgetter(1))[0]
    except Exception:
        pass
    
    output_text = open(os.path.join(output_dir, 'refseq_majority_organism.txt'),'w')
    output_text.write('Most likely organism from refseq_masher is {}\n'.format(major_org))

    refseq_success = 'refseq_masher program successfully ran on your input reads. ' \
        'refseq_masher output file (refseq.out), log file (refseq.log) and majority organism ' \
        '(refseq_majority_organism) written to ' + os.path.abspath(output_dir) + '.\n'
    
    return refseq_success


def main():
    
    if len(sys.argv) > 4 or len(sys.argv) < 3:
        sys.exit('''
        Command usage: python organism_detection.py OUTPUT_DIRECTORY FORWARD REVERSE
        Need to pass 3 arguments corresponding to output directory and forward 
        and reverse fastq reads. For a single read, only output directory and
        forward fastq read are required as arguments.
        ''')

    if len(sys.argv) == 4:
        output_dir = sys.argv[1]
        forward_read = sys.argv[2]
        reverse_read = sys.argv[3]
        
    elif len(sys.argv) == 3:
        output_dir = sys.argv[1]
        forward_read = sys.argv[2]
        reverse_read = None
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    string = refseq_masher_string(forward_read, reverse_read)

    try:
        refseq_out = refseq_masher_func(string, output_dir)
        complete = identify_organism(refseq_out, output_dir)
        sys.stdout.write(complete)

    except Exception as e:
        sys.stdout.write(str(e))

if __name__ == '__main__':
    main()
