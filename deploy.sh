#!/usr/bin/env bash

set -e

package_lambda() {
    echo
    echo "Creating Lambda zip package..."
    echo
    cd yumbot
    virtualenv env
    source env/bin/activate
    pip install -e .
    zip ../lambda.zip __init__.py main.py opentableclient.py yelpclient.py
    cd ../
}

deploy_bot() {
    echo
    echo "Deploying Lex bot..."
    echo
    cd lex/
    python lex.py
}

create() {
    echo "Deploying Lambda package..."
# Create Lambda function with zipped source
    package_lambda
    aws lambda create-function \
	--function-name aws-chatbot-lambda \
	--runtime python2.7 \
	--role arn:aws:iam::729905221641:role/aws-chatbot-lambda \
	--zip-file fileb://lambda.zip \
	--handler main.lambda_handler

	aws lambda add-permission \
	--function-name aws-chatbot-lambda \
	--statement-id LambdaLex \
	--action lambda:InvokeFunction \
	--principal lex.amazonaws.com \
	--source-arn "arn:aws:lex:us-east-1:729905221641:intent:*"
}

update_config() {
    echo "Updating Lambda function config..."
    aws lambda update-function-configuration \
	--function-name aws-chatbot-lambda \
	--handler main.lambda_handler
}

update_code() {
    package_lambda
    echo
    echo "Updating Lambda function code..."
    echo
    aws lambda update-function-code \
    --function-name aws-chatbot-lambda \
    --zip-file fileb://lambda.zip \
    --publish
}

if [[ $1 == "create" ]]; then
    create
elif [[ $1 == "update-config" ]]; then
    update_config
elif [[ $1 == "deploy-bot" ]]; then
    deploy_bot
else
    update_code
fi

exit 0