import os
import time
import boto3

def add_to_queue(contact_id, queue_name):
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['QUEUE_REGION'])
    table = dynamodb.Table(os.environ['QUEUE_TABLE'])
    table.put_item(
        Item={
            "contact_id": contact_id,
            "queue_name":  queue_name,
            "queue_started_time": str(round(time.time())),
            "queue_last_updated_time": str(round(time.time())),
        },
    )
    return True

def update_last_updated(contact_id):
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['QUEUE_REGION'])
    table = dynamodb.Table(os.environ['QUEUE_TABLE'])
    table.update_item(
        TableName=os.environ['QUEUE_TABLE'],
        Key={
            'contact_id': contact_id
        },
        UpdateExpression="set queue_last_updated_time = :queue_last_updated_time_value",
        ExpressionAttributeValues={
            ':queue_last_updated_time_value': str(round(time.time()))
        },
        ReturnValues="NONE"
    )
    return True

def remove_contact_from_queue(contact_id):
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['QUEUE_REGION'])
    table = dynamodb.Table(os.environ['QUEUE_TABLE'])
    table.delete_item(
        TableName=os.environ['QUEUE_TABLE'],
        Key={
        'contact_id': contact_id
        }
    )
    
def get_queue_position(contact_id, queue_name):
    dynamodb = boto3.client('dynamodb', region_name=os.environ['QUEUE_REGION'])
    update_last_updated(contact_id)
    
    operation_parameters = {
        "TableName": os.environ['QUEUE_TABLE'],
        "FilterExpression": "queue_name = :queue_name",
        "ExpressionAttributeValues": {
            ":queue_name": {"S": queue_name}
        },
    }
    
    data = {}
    
    paginator = dynamodb.get_paginator("scan")
    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        for item in page["Items"]:
            
            temp_started_time = item["queue_started_time"]["S"]
            temp_last_updated_time = int(item["queue_last_updated_time"]["S"])
            temp_contact_id = item["contact_id"]["S"]
            
            # Remove contact from queue if there has been no update in 60 seconds
            if (round(time.time()) - temp_last_updated_time) >= 60:
                remove_contact_from_queue(temp_contact_id)
                print(f"Contact {temp_contact_id} - has left the queue. Removing.")
            else:
                data[temp_contact_id] = int(temp_started_time)
                
    data = dict(sorted(data.items(), key=lambda item: item[1]))
    contact_position = list(data).index(contact_id) + 1
    print(f"Contact {contact_id} is number {contact_position} in the queue.")
    return {"queue_position": contact_position}