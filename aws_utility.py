#This file provides a set of utility functions for common operations in AWS:
#S3: Uploading, downloading (with optional deletion), and deleting files.
#SNS: Sending messages to topics.
#DynamoDB: Uploading items to a DynamoDB table.

import boto3


def delete_s3_file(bucket, key):    #key (file path) of the object 
    try:
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, key).delete()
    except Exception as e:
        raise Exception(e)


def get_file_from_s3(bucket_name, file_name, with_delete=False):
    try:
        s3 = boto3.client("s3")
        file_from_s3 = s3.get_object(Bucket=bucket_name, Key=file_name)
        file_content = file_from_s3["Body"].read().decode('utf-8-sig')    #decoded from UTF-8 with the utf-8-sig encoding, which helps handle files that may have a BOM (Byte Order Mark)

        if with_delete:
            delete_s3_file(bucket_name, file_name)

        return file_content, file_name

    except Exception as e:
        raise Exception(e)


def upload_to_s3(file_content, bucket_name, file_name):
    try:
        s3_resource = boto3.resource('s3')
        object_handler = s3_resource.Object(bucket_name, file_name)
        object_handler.put(Body=bytes(file_content, encoding="utf-8"))
    except Exception as e:
        raise Exception(e)


def send_sns_message(sns_topic_arn, sns_subject, sns_message):
    try:
        sns_client = boto3.client('sns')
        sns_client.publish(TopicArn=sns_topic_arn, Message=sns_message, Subject=sns_subject)
    except Exception as e:
        raise Exception(e)


def upload_to_dynamo(table_name, data_to_push):
    try:
        dynamodb_resource = boto3.resource('dynamodb')
        dynamodb_table = dynamodb_resource.Table(table_name)
        dynamodb_table.put_item(Item=data_to_push)
    except Exception as e:
        raise Exception(e)
