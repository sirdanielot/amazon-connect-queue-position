from aws_cdk import (
    CfnParameter,
    RemovalPolicy, 
    Stack
    aws_dynamodb as dynamodb
    aws_iam as iam
    aws_lambda as _lambda
    aws_s3 as s3
)

from constructs import Construct

class AmazonConnectQueuePosition(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        region = Stack.of(self).region

        # Parameters + Parameter Groups + Metadata Interface Formatting

        amazon_connect_id = CfnParameter(
            self,
            id="amazon-connect-id-param",
            default="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            min_length=36,
        )

        s3_bucket_name = CfnParameter(
            self, id="deployment-s3-bucket", default="deployment-bucket", min_length=1
        )

        deployment_lambda = CfnParameter(
            self, id="deployment-lambda-key", default="lambda.zip", min_length=1
        )

        self.template_options.metadata = {
            "AWS::CloudFormation::Interface": {
                "ParameterGroups": [
                    {
                        "Label": {"default": "Deployment Configuration"},
                        "Parameters": [
                            amazon_connect_id.logical_id,
                            s3_bucket_name.logical_id,
                            deployment_lambda.logical_id,
                        ],
                    },
                ],
                "ParameterLabels": {
                    amazon_connect_id.logical_id: {
                        "default": "Amazon Connect Instance ID"
                    },
                    s3_bucket_name.logical_id: {"default": "Deployment S3 Bucket"},
                    deployment_lambda.logical_id: {"default": "Lambda Zip Key"},
                },
            }
        }

        deployment_bucket = s3.Bucket.from_bucket_name(
            self, id="s3-bucket-lookup", bucket_name=s3_bucket_name.value_as_string
        )

        # DynamoDB Table
        amazon_connect_queue_position_table = dynamodb.Table(
            self,
            id="amazon-connect-queue-position",
            table_name="amazon-connect-queue-position",
            partition_key=dynamodb.Attribute(
                name="contact_id", type=dynamodb.AttributeType.STRING
            ),
            encryption=dynamodb.TableEncryption.AWS_MANAGED,
            removal_policy=RemovalPolicy.DESTROY,
        )

        lambda_role = iam.Role(
            self,
            id="amazon-connect-lambda-queue-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name="amazon-connect-lambda-queue-role",
            description="Role used by the Amazon Connect Queue Lambda Function",
        )

        lambda_role_policy = iam.Policy(
            self,
            id="amazon-connect-queue-lambda-policy",
            policy_name="amazon-connect-queue-lambda-policy",
            statements=[
                iam.PolicyStatement(
                    resources=[
                        f"arn:aws:dynamodb:*:*:table/{amazon_connect_queue_position_table.table_name}/index/*",
                        f"arn:aws:dynamodb:*:*:table/{amazon_connect_queue_position_table.table_name}",
                    ],
                    actions=[
                        "dynamodb:PutItem",
                        "dynamodb:DescribeTable",
                        "dynamodb:DeleteItem",
                        "dynamodb:GetItem",
                        "dynamodb:Scan",
                        "dynamodb:Query",
                        "dynamodb:UpdateItem",
                    ],
                ),
                iam.PolicyStatement(
                    resources=["arn:aws:logs:*:*:*"], actions=["logs:CreateLogGroup"]
                ),
                iam.PolicyStatement(
                    resources=["arn:aws:logs:*:*:log-group:/aws/lambda/*:*"],
                    actions=["logs:CreateLogStream", "logs:PutLogEvents"],
                ),
            ],
        )

        _lambda.Function(
            self,
            id="amazon-connect-queue-lambda",
            function_name="amazon-connect-queue-lambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_bucket(
                bucket=deployment_bucket, key=deployment_lambda.value_as_string
            ),
            handler="lambda_function.lambda_handler",
            environment={
                "QUEUE_TABLE": amazon_connect_queue_position_table.table_name,
                "QUEUE_REGION": region,
            },
            role=lambda_role,
        )

        lambda_role_policy.attach_to_role(lambda_role)
