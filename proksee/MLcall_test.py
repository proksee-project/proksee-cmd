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


# Case 1: Likely fair assembly
species = 'Streptococcus pyogenes'
n50 = 133891
contig_count = 42
l50 = 6
totlen = 1986343
gc_content = 0.383

"""
#Case 2: Likely great assembly
species = 'Staphylococcus aureus'
n50 = 574969
contig_count = 37
l50 = 2
totlen = 2791679
gc_content = 0.326
"""
"""
#Case 3: Likely great assembly
species = 'Listeria monocytogenes'
n50 = 481968
contig_count = 19
l50 = 3
totlen = 2877876
gc_content = 0.379
"""
"""
#Case 4: Likely poor assembly
species = 'Actinobacteria bacterium'
n50 = 4029
contig_count = 788
l50 = 195
totlen = 2475580
gc_content = 0.66
"""
"""
#Case 5: Likely poor assembly
species = 'Clostridioides difficile'
n50 = 44503
contig_count = 2593
l50 = 28
totlen = 4346150
gc_content = 0.293
"""
ml_instance = MachineLearningAssemQC(species, n50, contig_count, l50, totlen, gc_content)
probability = ml_instance.machine_learning_proba()
print(probability)
