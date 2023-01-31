# PageRank for multi-target drug discovery

This is an application of personalization-weight-PageRank in drug discovery. It is designed for simplify the calculation of molecular dynamics simulations between large numbers of proteins and small molecule drug/pharmacophores based on Markov decision process (MDP). We use PageRank by python library `NetworkX` for multi-target drug discovery.

# How to use it

The whole process of this research is in `experiment.py`. It is complex and have no graph.

`simple_example.py` contains a simple example of the experiment. It contains graphes and is easy for learning.

## Requirement
```
python = 3.8.10

NetworkX

Pandas

NumPy

SciPy

OpenPyXL

Matplotlib

jupyter

notebook
```

You could install the environment by conda:

`conda env create -f environment.yaml`

Then it will create a conda environment `pagerank`.

Or install it in other conda environment:

`conda install --yes --file requirements.txt`

We recommend use `jupyter notebook` extension of [VSCode](https://code.visualstudio.com/) for calculation. It is very intuitive.

## Data structure

The data has two parts:

1. The docking data is listed in `/data`. This means the affinity between drugs and targets.
2. The differentiation of targets by bioinformatics analysis. It is listed in the `.py` file.

## Protocol

1. Get all docking ranks of target proteins.
2. For different time group, calculate the rank of single drug respectively.
3. For different time group, calculate the rank of drug combinations.

## License

The license of this research is MPL-2.0.


## Citing this work

Liu F, Jiang X, Yang J, Tao J, Zhang M. A chronotherapeutics-applicable multi-target therapeutics based on AI: Example of therapeutic hypothermia. Brief Bioinform (2022).

M. Baek, et al., Accurate prediction of protein structures and interactions using a three-track neural network, Science (2021).

I.R. Humphreys, J. Pei, M. Baek, A. Krishnakumar, et al, Computed structures of core eukaryotic protein complexes, Science (2021).
