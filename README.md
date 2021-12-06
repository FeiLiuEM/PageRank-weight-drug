# Personalization-weight-PageRank-for-drug

This is an application of weighted PageRank in drug development. It's based on PageRank by python library `networkx`. Author used it to evaluate the influence between drugs and disease/therapy.

## Requirement

NetworkX

Pandas

NumPy

## Structure

The data has two layers: 1. The docking data of proteins and drugs listed in `/data/DATA.csv`. 2. The expression of proteins by bioinformatics analysis. In this research, we use experiment of hypothermia.

## Protocol
1. Get all docking ranks of target proteins.

2. At different time spot, compressive rank of all drugs of the expreiment.

3. Get rank of drug combination at different time spot of the experiment.
