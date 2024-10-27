import constants
import urllib
import aws_utility
import time
import transaction_processor
import os


print("Getting Values from environment variable")
try:
    DYNAMO_TABLE_NAME = os.environ['DYNAMO_TABLE_NAME']
    SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
    ERROR_BUCKET = os.environ['ERROR_BUCKET']
except Exception as error:
    print("Exception occurred while getting environment variable")
    print(error)


def lambda_handler(event, context):
    for record in event['Records']:

        if record['eventSource'] != 'aws:s3':
            print('Trigger is not from s3. Skipping Processing')
            return

        print("Trigger initiated from lambda")
        start_time = time.strftime('%Y%m%d_%H%M%S')

        print("Getting bucket name and filename")
        bucket_name = record['s3']['bucket']['name']

        # Get key replacing %xx of url-encoded value by equivalent character
        file_name = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding="utf-8")
        print(f"Trigger is due to file: {file_name} in bucket: {bucket_name}")

        try:
            print("Getting file content")
            sales_file_content, file_name = aws_utility.get_file_from_s3(bucket_name, file_name, with_delete=True)
        except Exception as e:
            end_time = time.strftime('%Y%m%d_%H%M%S')
            print('Error occurred while obtaining file content from s3.', e)
            error_message = f'Error reading file from s3. The error encountered is {str(e)}'
            print("Sending error notification to mail")
            aws_utility.send_sns_message(SNS_TOPIC_ARN, constants.FAILED_SNS_SUBJECT, error_message)

            dynamo_data = {'StartTime': start_time, 'EndTime': end_time, 'FileName': file_name, 'Status': 'Failure',
                           'FailureReason': str(e), 'ErrorPhase': 'Reading s3 content from the reprocess bucket'}

            print("Uploading error data in DynamoDB")
            aws_utility.upload_to_dynamo(DYNAMO_TABLE_NAME, dynamo_data)
            continue

        try:
            print(f"Aggregating data of file {file_name}")
            summarized_transaction, records_processed = transaction_processor.summarize_transaction(sales_file_content,
                                                                                                    file_name)
            print(f"Data of file: {file_name} aggregated.")
            print("Inserting aggregated data to database")
            transaction_processor.insert_to_rds(summarized_transaction)
            print("Data inserted into database")

        except Exception as e:
            end_time = time.strftime('%Y%m%d_%H%M%S')
            print(f'Error summarizing file: {file_name}.', e)
            aws_utility.upload_to_s3(sales_file_content, ERROR_BUCKET, file_name)

            error_message = f'Error occurred while processing the file: {file_name}. ' \
                            f'Please check error file in Bucket: {ERROR_BUCKET} with FileName: {file_name}.' \
                            f'\n\nThe error message encountered was {str(e)}'

            print("Sending notification message in mail")
            aws_utility.send_sns_message(SNS_TOPIC_ARN, constants.FAILED_SNS_SUBJECT, error_message)
            dynamo_data = {'StartTime': start_time, 'EndTime': end_time, 'FileName': file_name, 'Status': 'Failure',
                           'FailureReason': str(e), 'ErrorPhase': 'Summarizing transaction and inserting to RDS'}

            print("Uploading fail message in DynamoDB")
            aws_utility.upload_to_dynamo(DYNAMO_TABLE_NAME, dynamo_data)
            continue

        end_time = time.strftime('%Y%m%d_%H%M%S')
        print("Data Summarized Successfully")
        dynamo_data = {'StartTime': start_time, 'EndTime': end_time, 'FileName': file_name, 'Status': 'Success',
                       'RecordProcessed': records_processed}

        print("Uploading stat in DynamoDB")
        aws_utility.upload_to_dynamo(DYNAMO_TABLE_NAME, dynamo_data)
        success_message = f'File: {file_name} is processed successfully. Summarized data is on rds and log in dynamodb'
        print("Sending success to mail")
        aws_utility.send_sns_message(SNS_TOPIC_ARN, constants.SUCCESS_SNS_SUBJECT, success_message)
        print(f"File {file_name} aggregated successfully")
