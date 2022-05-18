# Assemble Tutorial

The following is a set of simple tutorials to illustrate how to run Proksee Assemble on a Linux command line and how to understand the outputs. Please ensure that you have already installed Proksee according the [installation instructions](../installation.md).

## Data

You will first need to obtain sequencing data to assemble. For this tutorial, we will be using *Vibrio cholerae* reads generated from an Illumina sequencing machine using a whole-genome sequencing strategy. The reads can be downloaded either by using NCBI's SRA Toolkit or downloading the reads directly from a web browser.

**Option 1: SRA Toolkit Download**

You will need to follow NCBI's instructions on how to [install](https://github.com/ncbi/sra-tools/wiki/02.-Installing-SRA-Toolkit) and [use](https://www.ncbi.nlm.nih.gov/sra/docs/sradownload/) the SRA Toolkit. We will download sequencing run SRR9201324 and, for the sake of simplicity, concatinate the pair-end reads into a single file.

```
fasterq-dump SRR9201324
cat SRR9201324_1.fastq SRR9201324_2.fastq > SRR9201324.fastq
```

The output file should be named "SRR9201324.fastq".

**Option 2: Web Browser Download**

You can download the reads directly from [this link](https://trace.ncbi.nlm.nih.gov/Traces/sra/?cmd=dload&run_list=SRR9201324&format=fastq). You will then need to extract and possibly rename the files:

```
gzip -d sra_data.fastq.qz
mv sra_data.fastq SRR9201324.fastq
```

## Setup

Activate the Proksee conda environment:

```
conda activate proksee
```

Check that Proksee can be run:

```
proksee assemble --help
```

If Proksee is installed correctly and the Conda environment activated correctly, you should see a help message reported:

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
  -t, --threads INTEGER   Specifies the number of threads programs in the
                          pipeline should use. The default is 4.
  -m, --memory INTEGER    Specifies the amount of memory in gigabytes programs
                          in the pipeline should use. The default is 4
  --help                  Show this message and exit.
```

If you see this output, then it is likely that Proksee is installed correctly and ready to be run.

## Running Proksee

If this is your first time running Proksee, you will likely need to download and install the Mash sketch database required by Proksee by running:

```bash
proksee updatedb
```

You can assemble the reads we downloaded earlier with the following command:

```
proksee assemble SRR9201324.fastq -o output/
```

This will initiate an assembly of the SRR9201324 *Vibrio cholerae* reads and place all outputs in a directory called "output".

## Standard Output

After running Proksee Assemble, output will be written to standard output and to the output directory. If you wish to see the full output, please expand the collapsed section below. The output will be explained part by part further below.

<details>
  <summary>Full Output</summary>

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
 
</details>

**Read Formatting**

```
The reads appear to be formatted correctly.
```

Proksee quickly checks to see if the reads appear to be correctly formatted. In our example, the reads appear to be formatted correctly.

**Sequencing Platform Identification**

```
Attempting to identify the sequencing platform from the reads.
Sequencing Platform: Unidentifiable
```

The software attempts to estimate the sequencing platform. However, as above, it is not always to uniquely identify the sequencing platform based on the FASTQ encoding and the platform is reported as "Unknown".

**Species Estimation**

```
Attempting to identify the species from the input.
SPECIES: Vibrio cholerae (p=1.00)

WARNING: Additional high-confidence species were found in the input data:

Vibrio albensis (p=1.00)
Atlantibacter hermannii (p=1.00)
Klebsiella michiganensis (p=1.00)
Erwinia amylovora (p=1.00)
```

The species is estimated using [Mash](https://github.com/marbl/Mash) and the species with the most evidence is selected. There may be additional high-confidence species reported. In this case, the species selected is *Vibrio cholerae*, but there are several other estimations (*Vibrio albensis*, *Atlantibacter hermannii*, etc.) with high confidence. As species estimation is somewhat inexact and complicated, we do not immediately flag the reads as being problematic, but instead verify the species again after contigs are assembled.

**Read Quality Check**

```
The read quality is acceptable.
```

The quality of the reads is evaluated using FASTP. If the quality is acceptable, then assembly will continue. In our example, the read quality appears to be acceptable.

**Fast Sequence Assembly**

```
Assembled reads using Skesa.
```

The reads are quickly assembled using Skesa.

**Species Verification**

```
PASS: The evaluated contigs appear to agree with the species estimation.
      The estimated species is: Vibrio cholerae (p=1.00)
```

A few of the largest contigs of the assembly each have their species estimated with RefSeq Masher. If the species estimated from each of these contigs is in agreement with the species estimated previously, then the assembly continues. It is possible that some data sets with contamination will continue in the pipeline, but as confident and automatic species estimation prove challenging, it is difficult to automate processes to handle low levels of contamination.

In the example above, since we previously estimated the species from the reads to be *Vibrio cholerae* and this agrees with the species estimated from each of the largest contigs (individually), then we proceed with sequence assembly.

**Machine Learning Assembly Evaluation**

```
Evaluated the quality of the assembled contigs.
The probability of the assembly being a good assembly is: 0.58.
```

The probability of the sequence assembly being "good" is estimating using our machine learning algorithm. Here we see that the probability of the assembly being "good" (i.e. similar to other RefSeq assemblies that we believe are good) is 58%.

**Heuristic Assembly Evaluation**

```
WARNING: The N50 is somewhat smaller than expected: 88901
         The N50 lower bound is: 47306.5
PASS: The number of contigs is comparable to similar assemblies: 104
      The acceptable number of contigs range is: (50.1, 265.9)
WARNING: The L50 is somewhat larger than expected: 15
         The L50 upper bound is: 26.9
WARNING: The assembly length is somewhat smaller than expected: 3939096
         The assembly length lower bound is: 3884870.0
```

The sequence assembly is the evaluated using a heuristic-based approach. The N50, number of contigs, L50, and assembly length are compared against the range of values for assemblies of that species and sequencing technology in our database of assemblies. The software reports a warning when the assembly measurement (N50, L50, etc.) is outside the 20-80 percentile range, and a failure when the measurement is outside the 5-95 percentile range.

In this case, we see that the number of contigs (104) seems comparable, but the N50 (88901), L50 (15), and assembly length (3,939,096) deviate somewhat from what is expect. However, their deviation is not too extreme, so warnings are issued and the assembly continues.

**Expert Assembly**

```
Performing expert assembly.
Assembled reads using SPAdes.
```

Using information collected in the previous steps, a strategy is determined for the "expert" assembly. The hope is that we can use information gathered from a fast Skesa assembly to better inform a more thorough assembly. In this case, SPAdes was selected to assembly the reads.

**Machine Learning Assembly Evaluation**

```
Evaluated the quality of the assembled contigs.
The probability of the assembly being a good assembly is: 0.89.
```

Proksee now evaluates the probability of the expert assembly being a good assembly (i.e. similar to assemblies in our RefSeq-derived assembly database) and reports that probability. There is an 89% probability that our expert assembly is similar to our RefSeq-derived assembly database.

**Heuristic Assembly Evaluation**

```
PASS: The N50 is comparable to similar assemblies: 108383
      The acceptable N50 range is: (47306.5, 375823.9)
PASS: The number of contigs is comparable to similar assemblies: 89
      The acceptable number of contigs range is: (50.1, 265.9)
PASS: The L50 is comparable to similar assemblies: 12
      The acceptable L50 range is: (4.0, 26.9)
PASS: The assembly length is comparable to similar assemblies: 3970349
      The acceptable assembly length range is: (3884870.0, 4184063.4)
```

The expert assembly is then evaluated using our heuristic approach, by comparing the assembly measurements against the percentile ranges for assemblies of the same species and sequencing techonology in our database.

In our example, all of the assemble measurements derived from the expert assembly appear normal, with respect to our database.

**Changes in Assemblies**

```
Changes in assembly statistics:
N50: 19482
Number of Contigs: -15
L50: -3
Length: 31253


Complete.
```

Finally, the changes in assembly measurements (N50, L50, etc.) between the fast assembly and the expert assembly are reported. In this case, we can see changes that suggest an improvement in assembly quality.

## Output Files

All output will be written to the specified output directory ("output" in our case). The output directory will contain the following files:

- **assembly_statistics.csv**: assembly statistics for the assemblies produced during pipeline
- **contigs.fasta**: the final contigs generated from the expert assembly
- **assembly_info.json**: a computer-readable, JSON-formatted file containing the information that was printed to standard output

The output directory may also contain output from various other programs called during execution of the pipeline, such as Quast and fastp.

