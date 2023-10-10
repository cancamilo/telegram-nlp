include .env
export

source_path=crypto_nlp/pos_labeled_data.csv
target_path=s3://my-nlp-datalake
profile=mlops

.PHONY: aws-login
aws-login:
	@aws sso login --sso-session ${profile}

.PHONY: copy-to-s3
copy-to-s3:
	@aws s3 cp ${source_path} ${target_path} --profile ${profile}

.PHONY: run-app
run-app:
	@python3 app/main.py	