import os
import sys
import subprocess, shlex


class Assembler():


    def __init__(self, forward, reverse, output_dir):
        self.forward = forward
        self.reverse = reverse
        self.output_dir = output_dir


    def __skesa_string(self):
        if self.reverse is None:
            skesa_str = 'skesa --fastq ' + self.forward + ' --use_paired_ends'
        else:
            skesa_str = 'skesa --fastq ' + self.forward + ',' + self.reverse
        
        return skesa_str


    def __skesa_func(self, skesa_str):
        skesa_out = open(os.path.join(self.output_dir,'skesa.out'), 'w+')
        skesa_log = open(os.path.join(self.output_dir,'skesa.log'), 'w+')
        try:
            rc = subprocess.check_call(skesa_str, shell=True, \
                stdout=skesa_out, stderr=skesa_log)
        except subprocess.CalledProcessError as e:
            raise e
        
        return rc
    
    
    def perform_assembly(self):
        skesa_string = self.__skesa_string()
        return_code = self.__skesa_func(skesa_string)
        output_string = 'SKESA assembled reads and log files written ' + \
            'to output directory. Return code {}'.format(return_code)
        
        return output_string

