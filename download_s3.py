import boto3


class S3Downloader:
    def __init__(self, bucket):
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket

    def download_file(self, key, local_filename):
        self.s3.Bucket(self.bucket_name).download_file(key, local_filename)

    def download_from_s3(self, key, path, filetype):
        if filetype == 'binary':
            s3_key = f'firmware/{key}.bin'
            local_filename = f'{path}/firmware.bin'
        elif filetype == 'dbc':
            s3_key = f'config/{key}.dbc'
            local_filename = f'{path}/{key}.dbc'
        else:
            raise ValueError('Invalid file type. Must be "binary" or "dbc".')

        self.download_file(s3_key, local_filename)


bucket_name = 'blackboxlinkedcar'
file_type = 'binary'  # or 'dbc'
file_name = 'firmware'  # or the name of the dbc file without extension
local_path = 'flash'

s3_downloader = S3Downloader(bucket_name)
s3_downloader.download_from_s3(file_name, local_path, file_type)
