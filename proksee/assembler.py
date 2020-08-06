import os
import sys
import subprocess, shlex


def skesa_string(fwd=None,rev=None):
    if rev is None:
        skesa_str = 'skesa --fastq ' + fwd + ' --use_paired_ends'
    elif rev.endswith('fastq') or rev.endswith('fq'):
        skesa_str = 'skesa --fastq ' + fwd + ',' + rev
    
    return skesa_str


def skesa_func(skesa_str=None, output_dir=None):
    skesa_out = os.path.join(output_dir,'skesa.out')
    skesa_log = os.path.join(output_dir,'skesa.log')
    stdout = open(skesa_out, 'w+')
    stderr = open(skesa_log, 'w+')
    try:
        subprocess.check_call(skesa_str, shell=True, stdout=stdout, stderr=stderr)
        skesa_success = 'Skesa program successfully ran on your input reads. ' \
        'Output assembly (skesa.out) and log file (skesa.log) written to ' \
        + os.path.abspath(output_dir) + '.\n'
    except subprocess.CalledProcessError as e:
        raise e

    return skesa_success


def main():

    if len(sys.argv) > 4 or len(sys.argv) < 3:
        sys.exit('''
        Command usage: python assembler.py OUTPUT_DIRECTORY FORWARD REVERSE
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

    string = skesa_string(forward_read, reverse_read)
    
    try:
        complete = skesa_func(string, output_dir)
        sys.stdout.write(complete)
    except Exception as e:
        sys.stdout.write(str(e))

if __name__ == '__main__':
    main()