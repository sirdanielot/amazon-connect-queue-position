# Importing Contact Flows


Replace the following values in your JSON files with the correct IDs from your instance:
 ```     
<instance_id> = Amazon Connect Instance ID
<region> = Amazon Connect Region
<CustomerQueue.wav Prompt ID> = The ID of the CustomerQueue.wav prompt
<customer_queue_flow_id> = The ID of the Customer Queue Flow
<customer_whisper_flow_id> = The ID of the Customer Whisper Flow
<queue_id> = The ID of the queue you wish to use
<queue_name> = The name of the queue you wish to use.
```

## Console
* Import the flows through the console.

## CLI
* Run the following commands
```
aws connect create-contact-flow --instance-id '<instance_id>' --name 'Customer Queue' --type 'CUSTOMER_QUEUE' --content "$(cat '1. Customer Queue.json')"
aws connect create-contact-flow --instance-id '<instance_id>' --name 'Customer Whisper' --type 'CUSTOMER_WHISPER' --content "$(cat '2. Customer Whisper.json')"
aws connect create-contact-flow --instance-id '<instance_id>' --name 'Inbound Flow' --type 'CONTACT_FLOW' --content "$(cat '3. Inbound Flow.json')"
```
