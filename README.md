# Crypto-NLP 

Welcome to the Crypto-NLP Tools project! This project is designed to demonstrate some Natural Language Processing (NLP) tasks using data scraped from social media channels. The notebooks and scripts in this repository aim demonstrate how the usage of AI can provide a deeper understanding of the crypto market trends and sentiments expressed across various social media platforms.

The project is strcutured as follows:

- [How to setup your environment](#how-to-setup-your-environment)
    - [Poetry](#poetry)
    - [Conda](#conda)
    - [Checking pytorch installation](#pytorch-environemnt-check)
    
- Data fetching (telegram-data-fetching.ipynb) and autolabeling
- Data Labeling with label studio (label-studio-setup.ipynb)
- Model inference and fine tuning (telegram_sentiment_fine_tuning_multiclass.ipynb)
- Fine tunning with hugging face and sagemaker
- Inference module
- RAG with telegram data
- Demo application
- Future work

## How to setup your environment

Depending on the script or notebook that you want to execute, there are two different ways to setup a python environemnt.
If pytorch is needed for training or inference, it is convient to use the conda environment. It specify the required dependencies to install pytorch on a Mac with M1/M2. For a different hardware setup, check the specific requirements. For scripts that do not make use of pytorch, the poetry environment is prefered as it is a more advance dependency managment tool.

### Poetry

Dependencies are Defined in the pyproject.toml file. 
To install just run: 

```console
poetry install
```
This environment should be used in all notebooks that do not have the pytorch dependency.

### Conda

Dependencies are defined in the torch-conda.yml file.
To create a conda environment from a yaml file:

```console
conda env create -f environment.yml
```

Other useful conda commands for managing environments:

to create a conda environemnt with a specific python version

```console
conda create -n tensorenv python=3.10
```

to activate the environment:

```console
conda activate tensorenv
```

to install a dependency inside the environment:

```console
conda install tesorflow
```

to remove a conda environment:

```console
conda env remove --name $env
```

### Pytorch environment check 

## AWS

### Login with AWS CLI

The detail process is detailed in this link:

https://docs.aws.amazon.com/singlesignon/latest/userguide/howtogetcredentials.html

The prerequisities are:

- Install the aws CLI

- You need to enable the IAM identity center service in your AWS acount. Then you will need to create a user, a permission set and assing that user to the permission set. 

- Execute `aws sso configure` to initiate a wizard that will guide you to the next steps. This step will create a configuration for the created user and will renew the credentials automatically when needed. 


### Common s3 commands

The aws cli commands need to include the `--profile {profile_name}`


### Dealing with external modules

The easiest way to enable using external modules is using the following code:

```
modules_path = os.path.join(os.getcwd(), "modules")
if modules_path not in sys.path:
    print("modules not in sys path. Inserting", modules_path)
    sys.path.insert(0, modules_path)
```

It works both for python scripts and notebooks. 

An alternative is to set the environemtn variable PYTHONPATH=${PWD}/your_module but it is not enough to set it in your python script or notebook with load_env(). It needs to be exported before. e.g source .env. Note that the variable has to be present in the .env file and it must have the keyword export in order to work.




