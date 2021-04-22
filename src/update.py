import json
import time
import logging
import os

from src import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def update(event, context):
    data = json.loads(event['body'])
    if 'user' not in data:# or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the user item.")
        return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # update the user in the database
    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
       # ExpressionAttributeNames={
        #  '#todo_text': 'text',
       # },
        ExpressionAttributeValues={
          ':email': data['email'],
          ':firstName': data['firstName'],
          ':lastName': data['lastName'],
          ':checked': data['checked'],
          ':updatedAt': timestamp,
        },
        UpdateExpression='SET email = :email, '
                         'checked = :checked, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response