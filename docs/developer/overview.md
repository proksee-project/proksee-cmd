# Developer Overview for Proksee

v1.0.0  
2021-04-08

Proksee is a Python 3 software project that provides a computational pipeline for performing sequence assembly, annotation, and visualization of microbial genomes. It is intented to be used by researchers who will have expertise in microbial genomics, but not necessarily bioinformatics or computational biology.

Proksee is implemented using object orientation priciples. It is comprised of multiple commands that that can be run individually or together in a larger computational pipeline. The complete Proksee pipeline would involve sequence assembly using `proksee assemble` and then sequence annotation and visualization using [Proksee's web interface](https://beta.proksee.ca/).

## File Organization

Proksee directories are organized as follows:

- **docs**: user and developer documentation
- **docs/developer**: developer documentation
- **proksee**: source files
- **tests**: test files

In addition, the following are notable files:

- **CHANGELOG**: log of notable changes made to the project
- **environment.yml**: programmatic instructions for installing a Proksee conda environment
- **LICENSE**: legal license for the project
- **MANIFEST.in**: non-source files to include in package installation
- **README.md**: short documentation targetted towards users
- **setup.py**: programmatic instructions for package installation
- **tox.ini**: programmatic instructions for running tox

## Commands

Proksee is comprised of the following commands:

- assemble
- evaluate

These commands are implemented using the [Click Python package](https://click.palletsprojects.com/en/7.x/). The entry point of the program is `proksee/cli.py`, which in turn calls the individual commands located in the `proksee/commands` directory.

Commands are invoked on the command line by entering the name of the program, proksee, followed by the name of the command being invoked. For example:

- `proksee assemble`
- `proksee evaluate`

