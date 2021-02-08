# Assemble

v1.0.0
2021-02-04

The assemble command is responsible for assembling sequencing reads into contigs. It uses an expert system to guide decision-making through the various stages of assembly.

## Pipeline

![overview](images/overview.png)

The assemble pipeline consists of three major stages:

- **Stage 1: Pre-Assembly**: Attempts to estimate information about the reads and prepares the reads for sequence assembly.
- **Stage 2: Fast Assembly**: Assembles the reads in a hastey manner in order to derive more information for expert assembly.
- **Stage 3: Expert Assembly**: Assembles the reads in an expert manner using information gathered during the previous stages.

## Pre-Assembly

![pre-assembly](images/pre_assembly.png)

The pre-assembly stage is responsible for estimating information about the reads, including the species and sequencing technology, and preparing the reads for sequence assembly.

### Validate Inputs

The forward and reverse read inputs are validated in order to ensure that they are in valid FASTQ format. The pipeline will terminate if the inputs appear to be formatted incorrectly.

### Identify Sequencing Platform

The sequencing platform is estimated by looking at the encoding of the FASTQ input reads. If there is not enough information to estimate the sequencing platform, then the platform will be unidentifiable, but assembly will continue. This stage is skipped if the user provides the sequencing platform as a command-line argument.

### Filter Reads

The reads are filtered in order to remove low-quality sequencing content and improve the assembly. FASTP is used to filter the reads.

### Determine Read Quality

The read quality is determined from the filtered reads by parsing the output of FASTP in the previous step. Since FASTP provides some quality metrics of the reads after filtering, this information is parsed into the pipeline and used in later steps.

### Estimate Species

Attempts to estimate the species using MASH. Since MASH is not designed to be a classifier, we shouldn't say that the species is *classified*, but rather the species is *estimated* from  *k*-mer information in the reads. MASH output can be messy on real-world data and will often report multiple species present in the data. High thresholds are therefore used in order to only report species that are very likely to be present. As a consequence of this approach, we cannot confidently make claims about low levels of contamination in the reads and thus ignore contamination.

## Fast Assembly

![fast assembly](images/fast_assembly.png)

The fast assembly stage consists of the following parts:

## Expert Assembly

![expert assembly](images/expert_assembly.png)

The expert assembly stage consists of the following parts:
