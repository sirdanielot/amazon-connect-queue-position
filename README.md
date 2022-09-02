# Amazon Connect Queue Position Solution

## Description

This solution allows you to keep track of each contact's position in the queue, and use this information to play a message while they are waiting in the queue.

Eg, "Thanks for waiting, you are the number x caller in the queue."

## Deployment
1. Create an S3 bucket that will be used for the CloudFormation deployment.
2. Upload [deployment/lambda.zip](https://github.com/danieljandey/amazon-connect-queue-position/blob/main/deployment/lamzda.zip) to the bucket.
3. Create a CloudFormation Stack using the template [deployment/amazon-connect-queue-position.template.json](https://github.com/danieljandey/amazon-connect-queue-position/blob/main/deployment/amazon-connect-queue-position.template.json)
4. Add the Lambda function under your Amazon Connect Instance (Amazon Connect -> Contact Flows -> AWS Lambda)
5. Upload the flows as through the console or CLI as instructed in [deployment/contact-flows/README.md](https://github.com/danieljandey/amazon-connect-queue-position/blob/main/deployment/contact-flows-README.md)
