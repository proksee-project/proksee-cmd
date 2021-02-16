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

"""Including a hypothetical assembly with species and metrics"""
species = 'Neisseria meningitidis'
#coverage = 100
n50 = 5373
l50 = 117
num_contigs = 1128
assembly_length = 2393084

machine_learning_instance = MachineLearningAssemQC(species, n50, num_contigs, l50, assembly_length)
probability = machine_learning_instance.machine_learning_proba()
print(probability)
