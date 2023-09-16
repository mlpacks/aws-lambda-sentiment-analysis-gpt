# AWS Lambda Function for Sentiment Analysis with GPT

A demonstration project and a ready-to-use template to deploy a AWS Lambda Function for sentiment analysis using GPT. You may easily adapt this project and use it for other tasks.

Sentiment analysis is a relative simple task for a Large-Language Model (LLM) like GPT. However, you may have to fine-tune the model for better performance in a given domain.

The simplicity and cost-efficiency of Lambdas make it worthwhile to consider for certain use cases. Specially when an API Gateway is needed to control and shared access to your "service".  

We hope you find this project useful and we welcome your feedback.

# Guide

This project is a ready-to-use template to create and deploy a working AWS Lambda using the [AWS Serverless Application Model (SAM)](https://aws.amazon.com/serverless/sam/).   

## Prerequisite
* Before you start, make sure you have installed the latest version of the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
and the [AWS Serverless Application Model (SAM)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).
* You will also need an [OpenAI API Key](https://beta.openai.com/docs/api-reference/authentication) to use the GPT model.
* Python 3.9 is required to build the project.

## Get a copy
```
git clone https://github.com/mlpacks/aws-lambda-sentiment-analysis-gpt.git
```

## Set your OpenAI API Key as an environment variable
```
export OPENAI_API_KEY=SET-YOUR-OPENAI-API-KEY-HERE
```

## Test the code locally
We made the code very simple to avoid any dependencies issues. A plain python environment is enough. To test, just run the following commands:
```
pushd src
python3 app.py
popd
```

If you set your key correctly, you should see:
```
{'text': 'The economic looks great.', 'sentiment': 'positive'}
```

## Python 3.9
If Python 3.9 is not your default python version, you can create a virtual environment with the following commands:
```
python3.9 -m venv venv
source venv/bin/activate
```

## Advanced users
You can skip the step by step instructions and go directly to the [Advanced users deployment](#advanced-users-deployment) section.


## Set some environment variables
To simplify the deployment process, let's create a couple of environment variables:
```
export AWSL_RAMDOM=$RANDOM-$RANDOM
export AWSL_STACK_NAME=awslambdas-sentiment-analysis-gpt
```

## Create a S3 bucket
AWS SAM need this to store some information about the deployment:
```
aws s3 mb s3://$AWSL_STACK_NAME-$AWSL_RAMDOM
```

## Build and deploy the Lambda
The Lambda to deploy is very simple. You can see the entire code in the file: ***src/app.py***. To have an idea, here is the lambda handler:
```python
import json
import http.client
import os

def lambda_handler(event, context):
    input_text = event["body"].strip()
    sentiment = classify_text(input_text)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "text": input_text,
            "sentiment": sentiment,
        }),
    }
```

Run the following commands to build and deploy the project to AWS:
```
sam build
sam deploy --stack-name $AWSL_STACK_NAME --s3-bucket $AWSL_STACK_NAME-$AWSL_RAMDOM --capabilities CAPABILITY_IAM --parameter-overrides OpenAPIKey=$OPENAI_API_KEY
```

## <a name="advanced-users-deployment" id="advanced-users-deployment"></a>Advanced users deployment
Advanced users that doesn't need to much of explanation can just run the following commands:
```
export OPENAI_API_KEY=SET-YOUR-OPENAI-API-KEY-HERE
export AWSL_RAMDOM=$RANDOM-$RANDOM
export AWSL_STACK_NAME=awslambdas-sentiment-analysis-gpt

aws s3 mb s3://$AWSL_STACK_NAME-$AWSL_RAMDOM

sam build
sam deploy --stack-name $AWSL_STACK_NAME --s3-bucket $AWSL_STACK_NAME-$AWSL_RAMDOM --capabilities CAPABILITY_IAM --parameter-overrides OpenAPIKey=$OPENAI_API_KEY
```

## Test your live Lambda Function
To test your Lambda, copy the value of the "API URL" from the previous command Outputs and you can call it with ***curl***:
```
curl -X POST -H "Content-Type: application/json" -d 'The economic looks great.' "API URL"
```

You should see the following response coming from your Lambda:
```json
{"text": "The economic looks great.", "sentiment": "positive"}
```

Congratulations! You have now a base Lambda project that you can use to build on top of it.

## Clean-up
To remove the Lambda and the Api Gateway, you just need to remove the stack:
```
aws cloudformation delete-stack --stack-name $AWSL_STACK_NAME
```

Wait a few seconds to allow the previous command to finish. Then, use the following commands to remove the s3 buckets.
```
aws s3 rb s3://$AWSL_STACK_NAME-$AWSL_RAMDOM --force
```