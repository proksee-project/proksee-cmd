# Proksee

Proksee is a suite of command line tools for performing genome [assembly](tools/assemble.md), [evaluation](tools/evaluate.md), annotation, and visualization of microbial genomes. Proksee is developed as a collaboration between the Public Health Agency of Canada, the University of Manitoba, and the University of Alberta. This resource provides information about the assembly and evaluation components of Proksee, whereas information about the annotation and visualization components may be found at [https://beta.proksee.ca/](https://beta.proksee.ca/).

## Release

v1.0.0a6

- Modifies the Mash database download procedure to write less output.
- Correctly instructs QUAST to use the user-specified minimum contig size.
- Better handling of Mash for species estimation of large assemblies with many contigs.
- Mash may now be run using parallelization.
- Removed possible security vulnerabilities when running subprocesses.
- Better user input checking.

## Contact

**Eric Enns**: eric.enns@canada.ca
