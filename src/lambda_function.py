from io import BytesIO
import boto3

def lambda_handler(event, context):
    # Get the name of the S3 bucket and the key for the file
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # Download the file from the S3 bucket
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    file_content = obj['Body']
    filename = BytesIO(file_content.read())
    return {
        "bucket": bucket,
        "key": key,
        "filename": filename,
        }