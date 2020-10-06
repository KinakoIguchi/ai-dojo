from __future__ import print_function
import boto3
from decimal import Decimal
import json
import urllib

print('Loading function')
rekognition = boto3.client('rekognition')
sns = boto3.client('sns')

# --------------- Helper Functions to call Rekognition APIs ------------------

def detect_faces(bucket, key):
    response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response


def detect_labels(bucket, key):
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})

    # Sample code to write response to DynamoDB table 'MyTable' with 'PK' as Primary Key.
    # Note: role used for executing this Lambda function should have write access to the table.
    #table = boto3.resource('dynamodb').Table('MyTable')
    #labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
    #table.put_item(Item={'PK': key, 'Labels': labels})
    return response


def index_faces(bucket, key):
    # Note: Collection has to be created upfront. Use CreateCollection API to create a collecion.
    #rekognition.create_collection(CollectionId='BLUEPRINT_COLLECTION')
    response = rekognition.index_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}}, CollectionId="BLUEPRINT_COLLECTION")
    return response


# --------------- Main handler ------------------


def lambda_handler(event, context):
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    print(event)
    key = event['Records'][0]['s3']['object']['key']
    try:
        # ToDo:imprements
        facedata = detect_faces(bucket, key)    # 要件によって使用するAPIが違うので、注意。
        print(facedata)
        ## ToDo:responseの中に顔の情報が載っているので、解析して出力できるような形にすること。
        msg =
        
        #SNSでトピックとして送信してあげる。　要件AB共通。
        TOPIC_ARN = 'arn:aws:sns:ap-northeast-1:096177927656:takao_itoi_RekognitionTopic'     
        subject = '課題A' # 件名。自分の挑戦した課題がわかるようにすること。
        response = sns.publish(
            TopicArn = TOPIC_ARN,
            Message = msg,
            Subject = subject
            )
            
        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e
        