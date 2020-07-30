import os
import sys
import subprocess, shlex


def fastp_string(fwd=None,rev=None, out=None):
    if rev == 'use_pair':
        fastp_str = 'fastp -i ' + fwd + ' -o ' + out
    elif rev.endswith('fastq') or rev.endswith('fq'):
        fastp_str = 'fastp -i ' + fwd + ' -I ' + rev + ' -o ' + out + ' -O ' + out
    
    return fastp_str


def fastp_func(fastp_str=None, fastp_out=None, fastp_log=None):
    fastp_out = open(fastp_out, 'w+')
    fastp_log = open(fastp_log, 'w+')
    subprocess.call(fastp_str, shell=True, stdout=fastp_out, stderr=fastp_log)


def main():
    forward_read = sys.argv[1]
    reverse_read = sys.argv[2]
    output = sys.argv[3]
    log = sys.argv[4]

    string = fastp_string(forward_read, reverse_read, output)
    
    fastp_func(string, output, log)

if __name__ == '__main__':
    main()
