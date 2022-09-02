#!/usr/bin/env python3
import aws_cdk as cdk
from cdk.amazon_connect_queue_position_stack import AmazonConnectQueuePosition

app = cdk.App()

account_id = app.node.try_get_context("account_id")
region = app.node.try_get_context("region")

if account_id == None or region == None:
    assert False, "Please enter a value for the account_id and region parameters.\n \
                   cdk synth -c account_id='' -c region=''"
else:
    AmazonConnectQueuePosition(
        app, 
        construct_id="amazon-connect-queue-position", 
        stack_name="amazon-connect-queue-position",
        env=cdk.Environment(
            account=account_id, 
            region=region
        ),
        synthesizer=cdk.DefaultStackSynthesizer(generate_bootstrap_version_rule=False)
    )

    app.synth()
