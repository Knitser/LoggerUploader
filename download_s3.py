import boto3


class S3Downloader:
    def __init__(self, bucket):
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket

    def download_file(self, key, local_filename):
        self.s3.Bucket(self.bucket_name).download_file(key, local_filename)

    def download_from_s3(self, key, path):
        downloader = S3Downloader(self)
        downloader.download_file(key, path)


bucket_name = 'blackboxlinkedcar'
s3_key = 'firmware/firmware.bin'
local_path = 'flash/firm.bin'

S3Downloader.download_from_s3(bucket_name, s3_key, local_path)
