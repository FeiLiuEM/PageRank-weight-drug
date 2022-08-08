# PageRank for multi-target drug discovery

This is an application of personalization-weight-PageRank in drug development. It is designed for simplified the calculation of molecular dynamics simulations between large numbers of proteins and small molecule drug/pharmacophores. It's based on PageRank by python library `networkx`. Authors used it for multi-target drug discovery.

# How to use it

The whole process of this research is in `experiment.py`. It is complex and have no graph.

`simple_example.py` contains a simple example of the experiment. It contains graphes and is easy for learning.

## Requirement

NetworkX

Pandas

NumPy

OpenPyXL

Matplotlib

## Data structure

The data has two parts:

1. The docking data is listed in `/data`. This means the affinity between drugs and targets.
2. The differentiation of targets by bioinformatics analysis. It is listed in the .py file.

## Protocol

1. Get all docking ranks of target proteins.
2. At different time spot, compressive rank of all drugs of the expreiment.
3. Get rank of drug combination at different time spot of the experiment.

# Citing this work

If you use the code or data in this package, please cite:

A chronotherapeutics-applicable multi-target therapeutics based on AI: the example of therapeutic hypothermia, Fei Liu et.al, Briefings in Bioinformatics, DOI:10.1093/bib/bbac365.
