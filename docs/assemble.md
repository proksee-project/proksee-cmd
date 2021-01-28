# Assemble

This pipeline assembles sequencing reads using expert system to guide decision-making through the various stages of sequence assembly. The pipeline consists of pre-assembly, fast assembly, and expert assembly stages.

## Stage 1: Pre-Assembly

As part of pre-assembly, the pipeline will validate inputs, attempt to identify the sequencing platform, filter reads, determine read quality, and estimate the species. If the inputs appear to be invalid (ex: incorrect sequencing encoding), then the program will terminate early.

## Stage 2: Fast Assembly

Fast assembly involves quickly assembling the reads in an approximate way to obtain information that will assist the later expert assembly. Fast assembly involves using the expert system to create an assembly strategy, assembling the reads with that strategy, evaluating the assembled contigs for contamination, and evaluating the fast assembly. The pipeline may terminate assembly during assembly strategy creation if there are multiple major species estimated in the reads. Similarly, when evaluating the assembled contigs for contamination, if any large contigs disagree with the previously estimated species, the pipeline will terminate.

## Stage 3: Expert Assembly

Expert assembly leverages the information obtained in the pre-assembly and fast assembly stages to produce a higher-quality assembly. This stage involves creating an assembly strategy, assembling the reads, evaluating the assembly, and finally generating a report by comparing the assembly to the fast assembly. The pipeline may terminate assembly during the creation of the assembly strategy if the assembly statistics (N50, L50, etc.) for the fast assembly appear to vary widely from what is expected for the assembled species.

## Basic Usage

```bash
proksee assemble [options] <forward reads> (<reverse reads>)
```

## Arguments

### Forward Reads

The FASTQ-formatted short-length forward reads to assemble. These reads may either be unpaired reads or the forward reads of paired-end reads.

### Reverse Reads

The FASTQ-formatted short-length reverse reads to assemble. This argument is optional and only provided as the pair to the forward reads provided in the previous argument.

## Options

```bash
-o , --output
```

The directory location to write output files. If this directory does not exist, then it will be created. Any files in this directory with the same name as any program output files will be overwritten.

### Force

```bash
--force
```

This flag forces the program to continue when the program would otherwise terminate. For example, it will force the program to continue assemble even if it appears there is considerable contamination or the fast assembly statistics look erroneous.

### Species

```bash
-s , --species
```

This option allows the user to specify the species in the reads to be assembled. The name must exactly match the scientific name for the species (ex: `--species 'Listeria monocytogenes'`). This will override any species estimation. If the passed species name does not match any species in the database, an error message will be displayed and the species will attempt to be estimated as normal.

### Platform

```bash
-p , --platform
```

The option allows the user to specify the sequencing platform that generated the reads. The name must be either: 'Illumina', 'Pac Bio', or 'Ion Torrent'. For example: `--platform 'Ion Torrent'`. If the passed platform name does not match a known platform, then the pipeline will attempt to estimate the platform from the reads as normal.

### Help

```bash
--help
```

Shows a help message and exits.

## Output

All output will be written to specified output directory or, if unspecified, the current directory. The output directory will contain the following files:

- assembly_statistics.csv: an overview of the assemblies produced during pipeline
- contigs.fasta: the final contigs generated from the expert assembly
- fwd_filtered.fastq: the forward filtered reads
- rev_filtered.fastq: the reverse filtered reads (if they exist)

The output directory may also contain output from various other programs called during execution of the pipeline.
