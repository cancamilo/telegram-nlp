# TODO list

## ML

- Implement the loading of the data from s3 [x]
- Follow along [this guide](https://huggingface.co/docs/sagemaker/getting-started) to start a fine tuning job on my data [x]

- Deploy an inference endpoint. (Optional) []

- Check different hugging face + sageaker notebook. [x]
    Take aways: 
    - there are several ways to optimize training jobs for cost and time reduction.
    - Models can be deployed with sage maker endpoints which can be expensive but using serverless inference might reduce the costs.
    - It can be used to traing LLMs.

    Optional Tasks:
    - For optimizing costs, consider Run training on a spot instances as described [here](https://github.com/huggingface/notebooks/blob/main/sagemaker/05_spot_instances/sagemaker-notebook.ipynb).  []

    - For optimizing cost, consider using sagemaker training compiler as done in [this notebook](https://github.com/huggingface/notebooks/blob/226b30b12d3f8102098cd3713a568954ca238936/sagemaker/15_training_compiler/sagemaker-notebook.ipynb). []



## Backend

- Implement logic to remember user session
    - Fix the login logic. If the session exists, and the user logs out, on logging again the flow will not work. [x]

## Frontend

- Find out how to deploy a simple frontend where the service can be used. e.g Giving a channel ID and getting the best/worst comments. [x]

## Other


- Fint out how to do a similar but more advanced service for semantic search in telegram channels. 
    - Investigate what kind of data is needed for this. []

- Expriment with fine tuning LAMA locally. Explained here https://www.youtube.com/watch?v=3fsn19OI_C8&ab_channel=AbhishekThakur

## Improvements to the sentiment classifier app

- Make useful notebooks into scripts:
    - Fetching telegram data for a list of channels. []
    - Autolabeling for sentiment classification with openAI []
    - Model training

- Website improvements:
    - Add dates to the messages for better reading []
    - Add message history for each of the messages dislayed []
    - Deploy to the cloud []
    - Show progress bar while waiting for the results. []
    - Add pagination to the message lists. []

## Semantic search

- Separate query encoding from documents encoding into functions. Create some modules for simplifying and organizing code.
- Build demo in the notebook with langchain or similar tools.



