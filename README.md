# Proksee

Proksee is a suite of command line tools for performing assembly, annotation and visualization of microbial genomes.  

Usage: `proksee assemble -o /path/to/output/directory FORWARD REVERSE`  

where the argument provided after -o lets a user to specify a desired output directory. `FORWARD` and `REVERSE`  are fastq sequencing read files. If `REVERSE` is not specified, only single strand (`FORWARD`) is processed by proksee pipeline.  
Currently `proksee` performs the following tasks:

- Checking for validity of fastq files. Both zipped and unzipped fastq files are acceptable.  
- Identification of sequencing platform (Illumina, Pacbio, others) based on input reads.  
- Filtering of reads using `fastp` which preprocesses and filters fastq files using a variety of quality metrics.    
- Identifying reference genome of the filtered sequence files using `refseq_masher`, which creates a Mash sketch   using MinHash algorithm and further processing of refseq_masher output to identify the most probable reference  genome organism.    
- Constructing a de-novo sequence assembly using `skesa`, which performs assembly on the filtered fastq read files using optimal k-mer length based on DeBruijn graphs.  

Users are recommended to install packages `fastp`, `refseq_masher` and `skesa` in a conda environment as follows:  
`conda env create -f environment.yml`
`conda activate proksee`






