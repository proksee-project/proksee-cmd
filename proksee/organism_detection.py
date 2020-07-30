import os
import sys
import subprocess, shlex


def refseq_masher_string(fwd=None,rev=None):
    if rev == 'use_pair':
        ref_str = 'refseq_masher matches ' + fwd
    elif rev.endswith('fastq') or rev.endswith('fq'):
        ref_str = 'refseq_masher matches ' + fwd + ' ' + rev
    
    return ref_str

def refseq_masher_func(ref_str=None, output_file=None, refseq_log=None):
    refseq_output = open(output_file, 'w+')
    reflog = open(refseq_log, 'w+')
    subprocess.call(ref_str, shell=True, stdout=refseq_output, stderr=reflog)


def main():
    forward_read = sys.argv[1]
    reverse_read = sys.argv[2]
    output_file = sys.argv[3]
    log = sys.argv[4]

    string = refseq_masher_string(forward_read, reverse_read)

    refseq_masher_func(string, output_file, log)

if __name__ == '__main__':
    main()
