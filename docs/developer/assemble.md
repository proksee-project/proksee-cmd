# Assemble

v1.0.0
2021-02-04

The assemble command is responsible for assembling sequencing reads into contigs. It uses an expert system to guide decision-making through the various stages of assembly.

## Pipeline

The assemble pipeline consists of three major stages:

- **Stage 1: Pre-Assembly**: Attempts to estimate information about the reads and prepares the reads for sequence assembly.
- **Stage 2: Fast Assembly**: Assembles the reads in a hastey manner in order to derive more information for expert assembly.
- **Stage 3: Expert Assembly**: Assembles the reads in an expert manner using information gathered during the previous stages.

## Pre-Assembly

The pre-assembly stage consists of the following parts:


