import handlers.dynamo_handler as dynamo_handler

def lambda_handler(event, context):
    contact_id = event['Details']['ContactData']['InitialContactId']
    queue = event['Details']['ContactData']['Queue']['Name']

    if 'Function' in event['Details']['Parameters']:
        function = event['Details']['Parameters']['Function']

        if function == 'add_to_queue':
            return dynamo_handler.add_to_queue(contact_id, queue)

        elif function == 'get_queue_position':
            return dynamo_handler.get_queue_position(contact_id, queue)

        elif function == 'remove_queue_position':
            return dynamo_handler.remove_contact_from_queue(contact_id)
    return True