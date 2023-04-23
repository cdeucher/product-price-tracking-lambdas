#!/bin/bash

export AWS_ACCESS_KEY_ID=dummy
export AWS_SECRET_ACCESS_KEY=dummy
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_OFFLINE=true

docker-compose up -d

awslocal sqs create-queue --queue-name titles --attributes file://tests/mock/fixtures/create-queue.json
$(awslocal dynamodb delete-table --table-name titles || true)
awslocal dynamodb create-table --cli-input-json file://tests/mock/fixtures/create-table.json
awslocal dynamodb put-item --table-name titles --item file://tests/mock/fixtures/put-item.json
awslocal dynamodb put-item --table-name titles --item file://tests/mock/fixtures/put-item2.json