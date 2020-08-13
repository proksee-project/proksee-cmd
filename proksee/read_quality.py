import os
import sys
import subprocess, shlex

class ReadFiltering():


    def __init__(self, forward, reverse, output_dir):
        self.forward = forward
        self.reverse = reverse
        self.output_dir = output_dir


    def fastp_string(self, forward, reverse, output_dir):
        out1 = os.path.join(output_dir, 'fwd_filtered.fastq')
        out2 = os.path.join(output_dir, 'rev_filtered.fastq')
        json = os.path.join(output_dir, 'fastp.json')
        html = os.path.join(output_dir, 'fastp.html')
        
        if reverse is None:
            fastp_str = 'fastp -i ' + forward + ' -o ' + \
                out1 + ' -j ' + json + ' -h ' + html
        elif reverse.endswith('fastq') or reverse.endswith('fq'):
            fastp_str = 'fastp -i ' + forward + ' -I ' + \
                reverse + ' -o ' + out1 + ' -O ' + \
                out2 + ' -j ' + json + ' -h ' + html
        
        return fastp_str


    def fastp_func(self, output_dir, fastp_str):
        fastp_log = open(os.path.join(output_dir, 'fastp.log'), 'w+')
        try:
            rc = subprocess.call(fastp_str, shell=True, stderr=fastp_log)    
        except subprocess.CalledProcessError as e:
            raise e

        return rc
        

    def filter_read(self, forward, reverse, output_dir):
        fastp_string = self.fastp_string(forward, reverse, output_dir)
        return_code = self.fastp_func(output_dir, fastp_string)
        output_string = 'FASTP filtered reads written to output directory. Return code {}'.format(return_code)

        return output_string