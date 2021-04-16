# Tutorial

The following is a set of simple tutorials to illustrate how to run Proksee on the command line and understand the outputs. Please ensure that you have already installed Proksee according the [installation instructions](installation.md).

## Assemble

### Data

You will first need to obtain data to assemble. For this tutorial, we will be using *Vibrio cholerae* reads generated from an Illumina sequencing machine using a whole-genome sequencing strategy. The reads can be downloaded either by using the SRA Toolkit or downloading the reads directly from a web browser.

**Option 1: SRA Toolkit Download**

You will need to follow the instructions on how to [install](https://github.com/ncbi/sra-tools/wiki) and [use](https://www.ncbi.nlm.nih.gov/sra/docs/sradownload/) the SRA Toolkit. We will be downloading sequencing run SRR9201324:

```
fasterq-dump SRR9201324
cat SRR9201324_1.fastq SRR9201324_2.fastq > SRR9201324.fastq
```

The output file should be named "SRR9201324.fastq".

**Option 2: Web Browser Download**

You can download the reads directoy from [this link](https://trace.ncbi.nlm.nih.gov/Traces/sra/?cmd=dload&run_list=SRR9201324&format=fastq). You will then need to unzip and possibly rename the files:

```
gzip -d sra_data.fastq.qz
mv sra_data.fastq SRR9201324.fastq
```

### Setup

Activate the Proksee conda environment:

```
conda activate proksee
```

Check that Proksee can be run:

```
proksee assemble --help
```

You should see a help message reported:

```
Usage: proksee assemble [OPTIONS] FORWARD [REVERSE]

Options:
  -o, --output DIRECTORY  [required]
  --force                 This will force the assembler to proceed when the
                          assembly appears to be poor.

  -s, --species TEXT      The species to assemble. This will override species
                          estimation. Must be spelled correctly.

  -p, --platform TEXT     The sequencing platform used to generate the reads.
                          'Illumina', 'Ion Torrent', or 'Pac Bio'.

  --help                  Show this message and exit.
```

If you see this output, then it is likely that Proksee is installed correctly and ready to be run.

### Running Proksee

You can assemble the reads we downloaded earlier with the following command:

```
proksee assemble SRR9201324.fastq -o output/
```

This will initiate an assembly of the SRR9201324 *Vibrio cholerae* reads and place all outputs in a directory called "output". After running Proksee Assemble, the following should be written to standard output:

```
The reads appear to be formatted correctly.

Attempting to identify the sequencing platform from the reads.
Sequencing Platform: Unidentifiable

Attempting to identify the species from the input.
SPECIES: Vibrio cholerae (p=1.00)

WARNING: Additional high-confidence species were found in the input data:

Vibrio albensis (p=1.00)
Atlantibacter hermannii (p=1.00)
Klebsiella michiganensis (p=1.00)
Erwinia amylovora (p=1.00)

The read quality is acceptable.

Assembled reads using Skesa.

PASS: The evaluated contigs appear to agree with the species estimation.
      The estimated species is: Vibrio cholerae (p=1.00)

Evaluated the quality of the assembled contigs.
The probability of the assembly being a good assembly is: 0.58.

WARNING: The N50 is somewhat smaller than expected: 88901
         The N50 lower bound is: 47306.5
PASS: The number of contigs is comparable to similar assemblies: 104
      The acceptable number of contigs range is: (50.1, 265.9)
WARNING: The L50 is somewhat larger than expected: 15
         The L50 upper bound is: 26.9
WARNING: The assembly length is somewhat smaller than expected: 3939096
         The assembly length lower bound is: 3884870.0

Performing expert assembly.
Assembled reads using SPAdes.
Evaluated the quality of the assembled contigs.
The probability of the assembly being a good assembly is: 0.89.

PASS: The N50 is comparable to similar assemblies: 108383
      The acceptable N50 range is: (47306.5, 375823.9)
PASS: The number of contigs is comparable to similar assemblies: 89
      The acceptable number of contigs range is: (50.1, 265.9)
PASS: The L50 is comparable to similar assemblies: 12
      The acceptable L50 range is: (4.0, 26.9)
PASS: The assembly length is comparable to similar assemblies: 3970349
      The acceptable assembly length range is: (3884870.0, 4184063.4)

Changes in assembly statistics:
N50: 19482
Number of Contigs: -15
L50: -3
Length: 31253


Complete.
```

