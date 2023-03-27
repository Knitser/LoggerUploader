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


class LogfileSplitter:
    def __init__(self, chunk_size):
        self.chunk_size = chunk_size

    def split_logfile(self, input_path):
        with open(input_path, 'rb') as f_in:
            file_size = os.path.getsize(input_path)
            print(f'Processing file {input_path} ({file_size} bytes)')

            # Split the logfile into chunks of `self.chunk_size` bytes
            chunks = [chunk for chunk in iter(lambda: f_in.read(self.chunk_size), b'')]

            # Save the chunks to separate gzip files
            for i, chunk in enumerate(chunks):
                chunk_size = len(chunk)
                filename = os.path.splitext(os.path.basename(input_path))[0]
                timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                output_path = f'zipfiles/{timestamp}_{filename}_{i}.gz'

                # Create a new gzip file for the chunk data
                with gzip.open(output_path, 'wb', compresslevel=9) as f_out:
                    # Write the chunk data to the output file
                    f_out.write(chunk)
                    print(f'Chunk {i} ({chunk_size} bytes) of file {input_path} successfully zipped')

                # Yield the chunk filename for uploading to S3
                yield output_path
