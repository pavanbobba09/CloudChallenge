import os
import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    result = table.update_item(
        Key={os.environ["PRIMARY_KEY"]: os.environ["PRIMARY_KEY_VALUE"]},
        UpdateExpression="SET #c = if_not_exists(#c, :start) + :one",
        ExpressionAttributeNames={"#c": "count"},
        ExpressionAttributeValues={
            ":start": Decimal(0),
            ":one": Decimal(1)
        },
        ReturnValues="UPDATED_NEW"
    )

    count = int(result["Attributes"]["count"])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"count": count})
    }
