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

Proksee can then be installed by running the setup script (when inside the Proksee directory):

```bash
pip install .
```
