#!/usr/bin/env bash
set -e
set -x

#build package

cd ~/git/splaysh-worker/
zip -r /tmp/splaysh-worker.zip . --exclude .git/\* .idea\*

#cd /usr/local/lib/python2.7/site-packages/
cd /usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages
zip -r  -u /tmp/splaysh-worker.zip .

#deploy s3

/usr/local/bin/aws --profile personal s3 cp /tmp/splaysh-worker.zip s3://splaysh-private-artifacts/splaysh-worker/;


#cycle lambda

aws lambda create-function \
--profile personal \
--region us-east-1 \
--function-name SplayshWorkerTwitter \
--code S3Bucket="splaysh-private-artifacts",S3Key="splaysh-worker/splaysh-worker.zip" \
--role arn:aws:iam::796019718156:role/splaysh-worker-lambda_dynamo  \
--handler twitter.main \
--runtime python2.7 \
--timeout 59 \
--memory-size 512 \
|| \
aws lambda update-function-code \
--profile personal \
--region us-east-1 \
--function-name SplayshWorkerTwitter \
--s3-bucket="splaysh-private-artifacts" \
--s3-key="splaysh-worker/splaysh-worker.zip"

##--zip-file fileb://tmp/splaysh-worker.zip \

echo "done!"
