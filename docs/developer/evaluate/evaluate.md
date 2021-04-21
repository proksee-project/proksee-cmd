# Proksee Evaluate Overview

v1.0.0  
2021-04-08

The evaluate command is responsible for evaluating sequence assemblies by comparing their assembly metrics to our database of assembly metrics for the same species. The command essentially implements only the evaluate stages of the full `proksee assemble` command, and it may be useful to reference that documentation for more information.

## Pipeline

The evaluate command consists of the following steps:

- estimate species
- measure assembly quality statistics
- heuristic evaluation
- machine learning evaluation

### Estimate Species

The species of the provided contigs is estimated if it is not also provided by the user. This is done using using MASH. Since MASH is not designed to be a classifier, we shouldn't say that the species is classified, but rather the species is estimated from k-mer information. Since we are operating on contigs instead of reads, we would expect to have a multiplicity of the species k-mers at approximately 1. We cannot use a strict filtering criteria for species estimation as we do for `proksee assemble`. It is therefore more likely that contamination may be reported as the species.

### Measure Assembly Quality Statistics

The assembly quality statistics are measured using QUAST. The pipeline uses a non-reference-based QUAST analysis, because of the difficulty of selecting a reference correctly and complication of needing to maintain either a database of references or the ability to download references on the fly. Several assembly metrics are collected, including N50, number of contigs, L50, and total assembly size.

### Heuristic Evaluation

A heuristic evaluation is performed by comparing the assembly quality measurements to a previously-built database of assembly statistics for various species. This database simply contains threshold levels, determined from percentiles of the original assembly statistics. The evaluation compares the calculated statistics against these thresholds and reports the results. For example, if most Listeria monocytogenes have an N50 between 2,500,000 and 3,500,000, but our Listeria monocytogenes assembly has an N50 of 2,000,000, then we would report to the user that there is a problem with the N50.

### Machine Learning Evaluation

A machine learning evaluation is performed by inputting the assembly statistics into a machine learning model. This model has been previously generated using the same data described in the heuristic evaluation. However, its methods are not the same. Please refer to the [machine learning documentation](../assemble/assemble.md) under Evaluate Assembly for more information
