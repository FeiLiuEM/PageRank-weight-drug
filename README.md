# PageRank-weight-drug

This is an application of weighted PageRank in drug development based on python. It's based on PageRank by python library `networkx`. Author used it to evaluate the influence between drugs and disease/therapy.

## Requirement

nxwork

pandas

numpy

## Structure

The data has two layers: 1. The docking data of proteins and drugs listed in `/data/DATA.csv`. 2. The expression of proteins by bioinformatics analysis. In this research, we use experiment of hypothermia.

## Protocol

1. Rank all the data of docking scores by protein expression.
