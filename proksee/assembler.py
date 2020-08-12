import os
import sys
import subprocess, shlex


class Assembler():


    def __init__(self, forward, reverse, output_dir):
        self.forward = forward
        self.reverse = reverse
        self.output_dir = output_dir


    def skesa_string(self, forward, reverse):
        if reverse is None:
            skesa_str = 'skesa --fastq ' + forward + ' --use_paired_ends'
        elif reverse.endswith('fastq') or reverse.endswith('fq'):
            skesa_str = 'skesa --fastq ' + forward + ',' + reverse
        
        return skesa_str


    def skesa_func(self, skesa_str, output_dir):
        skesa_out = open(os.path.join(output_dir,'skesa.out'), 'w+')
        skesa_log = open(os.path.join(output_dir,'skesa.log'), 'w+')
        try:
            subprocess.check_call(skesa_str, shell=True, \
                stdout=skesa_out, stderr=skesa_log)
        except subprocess.CalledProcessError as e:
            raise e

    def perform_assembly(self, forward, reverse, output_dir):
        skesa_string = self.skesa_string(forward, reverse)
        self.skesa_func(skesa_string, output_dir)
        output_string = 'SKESA assembled reads and log files written to \
            output directory'
        
        return output_string

