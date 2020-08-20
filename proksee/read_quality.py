import os
import sys
import subprocess, shlex

class ReadFiltering():


    def __init__(self, forward, reverse, output_dir):
        self.forward = forward
        self.reverse = reverse
        self.output_dir = output_dir


    def __fastp_string(self):
        out1 = os.path.join(self.output_dir, 'fwd_filtered.fastq')
        out2 = os.path.join(self.output_dir, 'rev_filtered.fastq')
        json = os.path.join(self.output_dir, 'fastp.json')
        html = os.path.join(self.output_dir, 'fastp.html')
        
        if self.reverse is None:
            fastp_str = 'fastp -i ' + self.forward + ' -o ' + \
                out1 + ' -j ' + json + ' -h ' + html
        else:
            fastp_str = 'fastp -i ' + self.forward + ' -I ' + \
                self.reverse + ' -o ' + out1 + ' -O ' + \
                out2 + ' -j ' + json + ' -h ' + html
        
        return fastp_str


    def __fastp_func(self, fastp_str):
        fastp_log = open(os.path.join(self.output_dir, 'fastp.log'), 'w+')
        try:
            rc = subprocess.check_call(fastp_str, shell=True, stderr=fastp_log)    
        except subprocess.CalledProcessError as e:
            raise e

        return rc
        

    def filter_read(self):
        fastp_string = self.__fastp_string()
        return_code = self.__fastp_func(fastp_string)
        output_string = 'FASTP filtered reads written to output directory. Return code {}'.format(return_code)

        return output_string