import os
import sys
import subprocess, shlex


def skesa_string(fwd=None,rev=None):
    if rev == 'use_pair':
        skesa_str = 'skesa --fastq ' + fwd + ' --use_paired_ends'
    elif rev.endswith('fastq') or rev.endswith('fq'):
        skesa_str = 'skesa --fastq ' + fwd + ',' + rev
    
    return skesa_str


def skesa_func(skesa_str=None, skesa_fasta=None, skesa_log=None):
    skesa_fasta = open(skesa_fasta, 'w+')
    skesa_log = open(skesa_log, 'w+')
    subprocess.call(skesa_str, shell=True, stdout=skesa_fasta, stderr=skesa_log)


def main():
    forward_read = sys.argv[1]
    reverse_read = sys.argv[2]
    skesa_fasta = sys.argv[3]
    skesa_log = sys.argv[4]
    
    string = skesa_string(forward_read, reverse_read)
    
    skesa_func(string, skesa_fasta, skesa_log)

    skesa_success = 'Skesa program successfully ran on your input reads. ' \
    'Assembly is in ' + skesa_fasta + \
    '. Log file is ' + skesa_log
    
    sys.stdout.write(skesa_success)

if __name__ == '__main__':
    main()