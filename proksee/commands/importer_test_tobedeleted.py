import os
import sys
from proksee import platform_identify
from proksee import read_quality
from proksee import organism_detection
from proksee import assembler

forward = sys.argv[1]
reverse = sys.argv[2]

file_dicn = platform_identify.fastq_extn_check(forward, reverse)
platform_dicn = platform_identify.platform_output(file_dicn)
print(platform_dicn)
sys.stdout.write('Platform identification complete\n')

fastp_output = sys.argv[3]
fastp_log = sys.argv[4]
fastp_string = read_quality.fastp_string(forward, reverse, fastp_output)
read_quality.fastp_func(fastp_string, fastp_output, fastp_log)
sys.stdout.write('Read quality assessment complete\n')


refseq_output = sys.argv[5]
refseq_log = sys.argv[6]
refseq_string = organism_detection.refseq_masher_string(forward, reverse)
organism_detection.refseq_masher_func(refseq_string, refseq_output, refseq_log)
sys.stdout.write('Organism detection complete\n')


skesa_output = sys.argv[7]
skesa_log = sys.argv[8]
skesa_string = assembler.skesa_string(forward, reverse)
assembler.skesa_func(skesa_string, skesa_output, skesa_log)
sys.stdout.write('Assembler (skesa) complete\n')