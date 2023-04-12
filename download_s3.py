import boto3
import os


class S3Downloader:
    def __init__(self, bucket, s3_prefix):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket
        self.s3_prefix = s3_prefix

    def download_latest_file(self, path):
        object_versions = self.s3.list_object_versions(Bucket=self.bucket_name, Prefix=self.s3_prefix)['Versions']
        latest_version = max(object_versions, key=lambda v: v['LastModified'])

        self.s3.download_file(self.bucket_name, latest_version['Key'], path)

        filename = os.path.basename(path)
        print(f'File {filename} ({os.path.getsize(path)} bytes) successfully downloaded from S3')


bucket_name = 'blackboxlinkedcar'
s3_prefix = "'logfiles/%Y/%m/%d/%H/'"
local_path = 'flash/firmware.bin'

downloader = S3Downloader(bucket_name, s3_prefix)
downloader.download_latest_file(local_path)
