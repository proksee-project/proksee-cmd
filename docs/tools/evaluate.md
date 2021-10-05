# Evaluate

The evaluate command evaluates the quality of sequence assemblies by comparing their various sequence assembly metrics to previous assemblies available in our database of the same species. It provides a report estimating the quality of the provided assembly. This command essentially performs only the evaluation part of `proksee assemble` and therefore allows users to evaluate assemblies directly.

!!! warning
    Proksee evaluate is designed to evaluate draft sequence assemblies and **not** complete genomes. The sort of assemblies that should be evaluated are those generated directly by sequence assembly tools. As complete genomes usually have very different assembly metrics (N50, number of contigs, etc.) from typical draft assemblies, it is difficult to evaluate a complete genome as a draft assembly.

## Basic Usage

**Command Line**

```bash
proksee evaluate [options] <contigs>
```

**Example**

```bash
proksee evaluate -o output contigs.fasta
```

## Arguments

### Contigs

The FASTA-formatted contigs representing a sequence assembly.

## Options

```bash
-o , --output
```

The directory location to write output files. If this directory does not exist, then it will be created. Any files in this directory with the same name as any program output files will be overwritten.

### Species

```bash
-s , --species
```

This option allows the user to specify the species of the assembly. The name must exactly match the scientific name for the species (ex: `--species 'Listeria monocytogenes'`). This will override any species estimation. If the passed species name does not match any species in the database, an error message will be displayed and the species will attempt to be estimated as normal.

### Help

```bash
--help
```

Shows a help message and exits.

## Output

All output will be written to the specified output directory. The output directory will contain the following files:

- **assembly_statistics.csv**: assembly statistics for the provided assembly

The output directory may also contain output from various other programs called during execution of the pipeline.
