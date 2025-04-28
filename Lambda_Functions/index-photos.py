import json
import boto3
import datetime
import requests
from requests_aws4auth import AWS4Auth

region = 'us-east-1'  # Update if needed
service = 'es'

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')

# Your OpenSearch endpoint
opensearch_host = 'https://search-photos-sbsbsbsbsabababa.aos.us-east-1.on.aws'

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        try:
            labels = get_labels(bucket, key)
            print("Detected Labels:", labels)

            document = {
                "objectKey": key,
                "bucket": bucket,
                "createdTimestamp": datetime.datetime.now().isoformat(),
                "labels": labels
            }

            index_photo(document, key)

        except Exception as e:
            print(f"Error processing {key}: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Photo processed and indexed successfully')
    }

def get_labels(bucket, key):
    # Rekognition labels
    rekog_response = rekognition_client.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': key}},
        MaxLabels=10,
        MinConfidence=75
    )

    labels = [label['Name'] for label in rekog_response['Labels']]

    # Custom labels from S3 object metadata
    metadata = s3_client.head_object(Bucket=bucket, Key=key)
    if 'Metadata' in metadata and 'customlabels' in metadata['Metadata']:
        custom_labels = [label.strip() for label in metadata['Metadata']['customlabels'].split(',')]
        labels.extend(custom_labels)

    return list(set(labels))  # Remove duplicates

def index_photo(document, key):
    url = f"{opensearch_host}/photos/_doc/{key}"
    headers = { "Content-Type": "application/json" }

    response = requests.put(url, auth=awsauth, headers=headers, json=document)
    print("OpenSearch Index Response:", response.text)
