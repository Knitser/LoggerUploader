import boto3
import gzip
import os
from datetime import datetime


class S3Uploader:
    def __init__(self, bucket_name, s3_prefix):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name
        self.s3_prefix = s3_prefix

    def upload_file(self, filepath):
        with open(filepath, 'rb') as f_in:
            filename = os.path.basename(filepath)
            self.s3.upload_fileobj(f_in, self.bucket_name, self.s3_prefix + filename)
            print(f'file {filename} ({os.path.getsize(filepath)} bytes) successfully uploaded to S3')
