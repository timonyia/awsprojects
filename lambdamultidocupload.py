import json
import boto3
import uuid
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

BUCKET_NAME = 'document-storage-bucket-unique-id'
TABLE_NAME = 'DocumentMetadata'

def lambda_handler(event, context):
    data = json.loads(event['body'])
    documents = data['documents']  # List of documents
    metadata = data['metadata']    # Metadata entered by user

    table = dynamodb.Table(TABLE_NAME)

    for document in documents:
        document_name = document['name']
        file_content = document['fileContent']
        document_id = str(uuid.uuid4())
        file_size = len(file_content)

        # Upload document to S3
        s3.put_object(Bucket=BUCKET_NAME, Key=document_id, Body=file_content)

        # Store metadata in DynamoDB
        table.put_item(Item={
            'documentId': document_id,
            'documentName': document_name,
            'department': metadata['department'],
            'description': metadata['description'],
            'fileSize': file_size,
            'uploadTime': datetime.utcnow().isoformat()
        })

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Documents uploaded successfully'})
    }
