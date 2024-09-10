import json
import boto3

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

BUCKET_NAME = 'document-storage-bucket-unique-id'
TABLE_NAME = 'DocumentMetadata'

def lambda_handler(event, context):
    query_params = event['queryStringParameters']
    document_name = query_params.get('documentName', None)
    department = query_params.get('department', None)

    table = dynamodb.Table(TABLE_NAME)

    # Scan DynamoDB with filters
    scan_kwargs = {}
    if document_name:
        scan_kwargs['FilterExpression'] = boto3.dynamodb.conditions.Attr('documentName').eq(document_name)
    if department:
        scan_kwargs['FilterExpression'] = boto3.dynamodb.conditions.Attr('department').eq(department)

    response = table.scan(**scan_kwargs)
    items = response['Items']

    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
