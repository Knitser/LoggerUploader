import boto3
import gzip
import os
from datetime import datetime
import subprocess

subprocess.run(['pip', 'install', '-r', 'requirements.txt'])


class S3Uploader:
    def __init__(self, bucket_name, s3_prefix):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name
        self.s3_prefix = s3_prefix

    def upload_chunk(self, filepath):
        with open(filepath, 'rb') as f_in:
            filename = os.path.basename(filepath)
            self.s3.upload_fileobj(f_in, self.bucket_name, self.s3_prefix + filename)
            print(f'Chunk {filename} ({os.path.getsize(filepath)} bytes) successfully uploaded to S3')


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
                output_path = f'zipfiles/{i}_{os.path.basename(input_path)}.gz'

                # Create a new gzip file for the chunk data
                with gzip.open(output_path, 'wb', compresslevel=9) as f_out:
                    # Write the chunk data to the output file
                    f_out.write(chunk)
                    print(f'Chunk {i} ({chunk_size} bytes) of file {input_path} successfully zipped')

                # Yield the chunk filename for uploading to S3
                yield output_path


def main():
    s3_uploader = S3Uploader('blackboxlinkedcar', datetime.now().strftime('logfiles/%Y/%m/%d/%H/'))
    logfile_splitter = LogfileSplitter(chunk_size=2 * 1024 * 1024)

    # Create the zipfiles directory if it doesn't exist
    if not os.path.exists('zipfiles'):
        os.makedirs('zipfiles')

    # Delete the previous log files
    for filename in os.listdir('zipfiles'):
        os.remove(os.path.join('zipfiles', filename))
        print('Old zipfiles successfully removed')

    # Split each logfile into smaller parts and upload them individually
    for filename in os.listdir('logfiles'):
        input_path = os.path.join('logfiles', filename)
        for chunk_path in logfile_splitter.split_logfile(input_path):
            s3_uploader.upload_chunk(chunk_path)

    print('All logfiles successfully uploaded to S3')


if __name__ == '__main__':
    main()
