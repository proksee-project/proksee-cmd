# Installation

Proksee requires that the following software packages be installed:

- Python 3.7
- Pip
- fastp
- Refseq Masher
- Skesa
- Quast
- Scipy
- Spades

The simplest way to install these packages, and any other related dependencies, is by installing them into a conda environment, using the provided installation script as follows:

```bash
conda env create -f environment.yml
conda activate proksee
```

You can then confirm that Proksee is installed with the following command, which should show a help message:

```bash
proksee --help
```
