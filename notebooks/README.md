# Crypto NLP 

The goal of this project is to perform several NLP tasks such as text classifiation, summarization annd semantic sarch on cryptocurrency data. Data soources include telegram data, cryptocurrency news APIs and coinmarket cap scrappped data.


## Environments

There are two different ways to setup a python environemnt:

### Poetry

Dependencies are Defined in the pyproject.toml file. 

To install just run ```poetry install```

### Conda

It is neccesary to have an additional way to setup the environment with conda since it supports pytorch and tensorflow.


#### Pytorch

create conda env:

```conda env create -f torch-conda-nightly.yml -n torch```

The yml is provided in this repo.

Pytorch can perform training and inference using different type of hardware. 

In order to check your hardare run the nootebooks for fine tuning.


#### Tensorflow

to create a conda environemnt with a specific python version

```conda create -n tensorenv python=3.10```

to activate the environment:

```conda activate tensorenv```

to install a dependency inside the environment:

```conda install tesorflow```

## TODO's

1. Form a thread by getting all the previous messages for a particular message. Useful for interpreting the sentiment of a comment. [x].

2. Fine tune some model with the labeled data, make it binary. [x]

3. Compare the labeled dataset to a binary classifier. [x]





