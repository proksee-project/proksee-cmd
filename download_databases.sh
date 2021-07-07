#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DATABASE_DIR="$SCRIPT_DIR/proksee/database"
MASH_SKETCH="$DATABASE_DIR/refseq.genomes.k21s1000.msh"

wget -O $MASH_SKETCH https://gembox.cbcb.umd.edu/mash/refseq.genomes.k21s1000.msh

