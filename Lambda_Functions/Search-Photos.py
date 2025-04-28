import json
import boto3
import requests
from requests_aws4auth import AWS4Auth

region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# OpenSearch endpoint
opensearch_host = 'https://search-photos-abababababababababa.aos.us-east-1.on.aws'

def lambda_handler(event, context):
    print("Received event:", json.dumps(event, indent=2))

    keywords = []
    frontend_request = False  # Flag to distinguish

    if 'queryStringParameters' in event and event['queryStringParameters']:
        if 'q' in event['queryStringParameters']:
            raw_query = event['queryStringParameters']['q']
            keywords = [word.capitalize() for word in raw_query.split()]
            frontend_request = True   # 📢 Marking frontend case

    elif 'sessionState' in event and 'intent' in event['sessionState']:
        slots = event['sessionState']['intent']['slots']
        if slots and 'keyword' in slots and slots['keyword']:
            raw_query = slots['keyword']['value']['interpretedValue']
            keywords = [word.capitalize() for word in raw_query.split()]

    print("Search keywords:", keywords)

    if not keywords:
        if frontend_request:
            return {
                'statusCode': 200,
                'headers': { "Access-Control-Allow-Origin": "*" },
                'body': json.dumps({ "results": [] })
            }
        else:
            return {
                "sessionState": {
                    "dialogAction": { "type": "Close" },
                    "intent": { "name": "SearchIntent", "state": "Fulfilled" }
                },
                "messages": [ { "contentType": "PlainText", "content": "No keywords provided to search." } ]
            }

    # Perform OpenSearch query
    search_url = f"{opensearch_host}/photos/_search"
    headers = { "Content-Type": "application/json" }
    query = {
        "size": 100,
        "query": {
            "terms": {
                "labels.keyword": keywords
            }
        }
    }

    response = requests.get(search_url, auth=awsauth, headers=headers, json=query)
    print("OpenSearch response:", response.text)
    response_json = response.json()

    results = []
    for hit in response_json['hits']['hits']:
        source = hit['_source']
        results.append({
            'objectKey': source['objectKey'],
            'bucket': source['bucket'],
            'createdTimestamp': source['createdTimestamp'],
            'labels': source['labels']
        })

    # Now return correctly based on who asked
    if frontend_request:
        return {
            'statusCode': 200,
            'headers': { "Access-Control-Allow-Origin": "*" },
            'body': json.dumps({ "results": results })
        }
    else:
        return {
            "sessionState": {
                "dialogAction": { "type": "Close" },
                "intent": { "name": "SearchIntent", "state": "Fulfilled" }
            },
            "messages": [
                { "contentType": "PlainText", "content": f"Found {len(results)} matching photos!" if results else "No matching photos found." }
            ]
        }
