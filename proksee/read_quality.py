import os
import sys
import subprocess, shlex


def fastp_string(fwd=None,rev=None, output_dir=None):
    out1 = os.path.join(output_dir, 'fwd_filtered.fastq')
    out2 = os.path.join(output_dir, 'rev_filtered.fastq')
    json = os.path.join(output_dir, 'fastp.json')
    html = os.path.join(output_dir, 'fastp.html')
    
    if rev is None:
        fastp_str = 'fastp -i ' + fwd + ' -o ' + out1 + \
                    ' -j ' + json + ' -h ' + html
    elif rev.endswith('fastq') or rev.endswith('fq'):
        fastp_str = 'fastp -i ' + fwd + ' -I ' + rev + ' -o ' + out1 + ' -O ' + \
                    out2 + ' -j ' + json + ' -h ' + html
    
    return fastp_str


def fastp_func(fastp_str=None, output_dir=None):
    fastp_log = os.path.join(output_dir, 'fastp.log')
    stderr = open(fastp_log, 'w+')
    try:
        subprocess.call(fastp_str, shell=True, stderr=stderr)
        fastp_success = 'FASTP program successfully ran on your input reads. ' \
        'Output reads (fwd/rev_filtered.fastq), log file (fastp.log) and other ' \
        'output files(fastp.json and fastp.html) written to ' + os.path.abspath(output_dir) + '.\n'
    except subprocess.CalledProcessError as e:
        raise e

    return fastp_success


def main():

    if len(sys.argv) > 4 or len(sys.argv) < 3:
        sys.exit('''
        Command usage: python read_quality.py OUTPUT_DIRECTORY FORWARD REVERSE
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

    string = fastp_string(forward_read, reverse_read, output_dir)
    
    try:
        complete = fastp_func(string, output_dir)
        sys.stdout.write(complete)
    except Exception as e:
        sys.stdout.write(str(e))

if __name__ == '__main__':
    main()
