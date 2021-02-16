'''
Copyright:

University of Manitoba & National Microbiology Laboratory, Canada, 2020

Written by: Arnab Saha Mandal

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
'''

from machine_learning_assembly_qc import MachineLearningAssemQC

species = 'Neisseria meningitidis'
coverage = 100
n50 = 5373
contig_count = 1128
l50 = 117
totlen = 2393084

ml_instance = MachineLearningAssemQC(species, coverage, n50, contig_count, l50, totlen)
probability = ml_instance.machine_learning_proba()
print(probability)
