
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






## Environments

There are two different ways to setup a python environemnt:

### Poetry

Dependencies are Defined in the pyproject.toml file. 

To install just run ```poetry install```

### Conda

It is neccesary to have an additional way to setup the environment with conda since it supports pytorch and tensorflow.

to create a conda environemnt with a specific python version

```conda create -n tensorenv python=3.10```

to activate the environment:

```conda activate tensorenv```

to install a dependency inside the environment:

```conda install tesorflow```

to create a conda environment from a yaml file:

```conda env create -f environment.yml```

to remove a conda environment:

```conda env remove --name $env```

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

## TODO's

- Form a thread by getting all the previous messages for a particular message. Useful for interpreting the sentiment of a comment. Done.

- Compare the labeled dataset to the pretrained model in the colab. Find some performance metrics.

- Fine tune some model with the labeled data

- Repeath the steps above to check if the fine tuned model has improved.

Note that all of the above makes sense if the labeled data has a good quality so I should check that first...




