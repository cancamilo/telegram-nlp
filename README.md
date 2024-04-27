# Crypto-NLP 

Welcome to the Crypto-NLP Tools project! This project is designed to showcase some natural language processing (NLP) tasks using data scraped from social media channels. The notebooks and scripts in this repository aim to demonstrate how the usage of machine learning can provide a deeper understanding of the crypto market trends and sentiments expressed across various social media platforms.

The project is strcutured as follows:

- [How to setup your environment](#how-to-setup-your-environment)
    - [Poetry](#poetry)
    - [Conda](#conda)
    - [Checking pytorch installation](#pytorch-environment-check)

- [Sentiment Classification](#sentiment-classification)
    - [Data fetching and autolabeling](#data-fetching-and-autolabeling)
    - [Data Labeling with label studio](#data-labeling-with-label-studio)
    - [Model inference and fine tuning](#model-inference-and-fine-tuning)
    - [Fine tunning with hugging face and sagemaker](#fine-tunning-with-hugging-face-and-sagemaker)
    - [Inference module](#inference-module)

- [RAG with telegram data]
- Demo application
- Future work

## How to setup your environment

Depending on the script or notebook that you want to execute, there are two different ways to setup a python environemnt.
If pytorch is needed for training or inference, it is convient to use the conda environment. It specify the required dependencies to install pytorch on a Mac with M1/M2. For a different hardware setup, check the specific requirements. For scripts that do not make use of pytorch, the poetry environment is prefered as it is a more advance dependency managment tool.

Note that you also need docker installed in your machine in order to run label-studio.

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

The installation of the pytorch dependencies can be verified by executing [this notebook](/notebooks/torch_test.ipynb). The code loads a standard dataset and uses it to fine tune a pretrained model.

### Telegram login

Some of the code requires to have access to telegram data. You need to be registered to telegram and acquire an API ID, API hash, phone number and username. All these variables can be set in the .env file. Refer to [this file](example.env) to fill in the required variables.

### AWS

Some of the notebooks in this repository can only be executed on the aws sagemaker environenment. This requires setting up an aws account.

### Login with AWS CLI

The detail process is detailed in this link:

https://docs.aws.amazon.com/singlesignon/latest/userguide/howtogetcredentials.html

The prerequisities are:

- Install the aws CLI

- You need to enable the IAM identity center service in your AWS acount. Then you will need to create a user, a permission set and assing that user to the permission set. 

- Execute `aws sso configure` to initiate a wizard that will guide you to the next steps. This step will create a configuration for the created user and will renew the credentials automatically when needed. 


Note: the aws cli commands need to include the `--profile {profile_name}`

## Sentiment classification

Classifying messages of social media channels can provide insights into the general cryptocurrency market sentiment and the overall community sentiment towards a specific cryptocurrency project. 

This section summarizes the tools for fetching, labeling and model training for the purpose of sentiment classification.

## Data fetching and autolabeling

The first task is to fetch data from several telegram cryptucurrency channels and label each message as either positive, neutral or negative. The labeled dataset is then used to train a sentiment classifier model. The process can be reproduced by executing the [telegram_data_detching notebook](/notebooks/telegram_data_fetching.ipynb). Note that for this step, an openai key is required in order to perform the autolabeling of the dataset. 

The output of this notebook should be two different csv file:

- data/chat_messages_clean.csv: fetched messages with some cleaning without labeling.
- labeled/prediction_df_{start}_{end}.csv: multiple csv files with labeled messages that will serve as the input for training a classification model.

## Data Labeling with label studio

As an alternative to the previous labeling process, we can make use of label studio for assigning classes to our message samples.

Label studio can be run by executing 

```console
docker-compose -f label-studio/labelstudio-docker-compose.yml up -d
```

This command will spin up several services required to run label studio.

The next step is to execute the [label studio project setup notebook](/notebooks/label-studio-setup.ipynb). This code will read the previously fetched raw data (data/chat_messages_clean.csv), create a new project for text classification and append the raw data to it.

Now we can navigate to [http:localhost:8080] where we have access to label studio UI. Under projects we will find the previously created project and we can start manually labeling the data.

Instead of manually labeling the messages, we can use the ML backend service which utilizes gtp 3.5 in the background to make predictions on our dataset. The service can provide us with predictions on our entire dataset on demand. To achieve this, follow [this guide](https://labelstud.io/blog/automate-data-labeling-with-llms-and-prompt-interface/).

## Model inference and fine tuning

With our labeled data we can proceed to fine tune a pretrained model. I chose the `distilbert-base-uncased` for finetuning which is a lighter and faster version of the BERT model and sufficient for the purpose of this project. 

The notebook for [fine-tunning](/notebooks/telegram_sentiment_fine_tuning_multiclass.ipynb) extracts all the labeled datasets found under the `notebooks/labeled` folder or any other location where the labeled data is saved. 

Initially, a previously pretrained model for sentiment classification without fine tuning is used to check some metrics. Then the `distilbert-base-model`is fine tuned with the telegram labeled data. 

With 5000 samples, a significant improvement is obtained by finetuning over using a default model. This process can be iterated with more data to obtain better performance.

## Fine tunning with hugging face and sagemaker

To simplify environemnt setup and accelerate training, we can also make use of AWS sagemaker to train our classifier. 

[The hugging face aws notebook](/notebooks/hugging_face_sagemaker_training.ipynb) provides the code to achieve this.

You can also follow [this guide](https://huggingface.co/docs/sagemaker/en/getting-started) for more specific details.

## Inference module

The inference module is used to perform sentiment predictions on a given test or validation messages dataset. [The inference notebook](/notebooks/simple_inference.ipynb) demonstrates the usage of the [module](/modules/sentiment_predictor.py). 


### Dealing with external modules

The easiest way to enable using external modules in python scripts and notebooks is using the following code:

```
modules_path = os.path.join(os.getcwd(), "modules")
if modules_path not in sys.path:
    print("modules not in sys path. Inserting", modules_path)
    sys.path.insert(0, modules_path)
```

An alternative is to set the environment variable PYTHONPATH=${PWD}/your_module but it is not enough to set it in your python script or notebook with load_env(). It needs to be exported before. e.g source .env. Note that the variable has to be present in the .env file and it must have the keyword export in order to work.




