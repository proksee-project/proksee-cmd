# Proksee

Proksee is a suite of command line tools for performing assembly, annotation and visualization of microbial genomes.

## Release

v1.0.0

This is the initial public release of Proksee. This release focuses on Proksee Assemble, the sequence assembly component of Proksee.

## Installation

Proksee requires the following packages:

- fastp
- refseq_masher
- skesa
 
This can be accomplished by installing dependencies into a conda environment, using the provided installation script as follows:

```bash
conda env create -f environment.yml
conda activate proksee
```

Proksee can then be installed by running the setup script (when inside the Proksee directory):

```bash
pip install .
```
## Assemble

The assemble pipeline consists of three major stages:

- **Stage 1: Pre-Assembly**: Verifies inputs, estimates information about the reads, filters the reads, and prepares the reads for sequence assembly.
- **Stage 2: Fast Assembly**: Assembles the reads quickly in order to derive structural information for expert assembly.
- **Stage 3: Expert Assembly**: Assembles the reads in an expert manner using information gathered during the previous stages.

**Command**

```bash
proksee assemble -o /path/to/output/directory FORWARD REVERSE
```

Where the argument provided after -o lets a user to specify a desired output directory. `FORWARD` and `REVERSE`  are fastq sequencing read files. If `REVERSE` is not specified, only single strand (`FORWARD`) is processed by the Proksee pipeline.  

**Example**

```bash
proksee assemble -o output forward_reads.fastq reverse_reads.fastq
```

## Contact

**Eric Enns**: eric.enns@canada.ca

## Legal

Copyright Government of Canada 2020-2021

Written by: National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except in compliance with the License. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
