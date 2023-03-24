import boto3
import gzip
import os
from datetime import datetime

s3 = boto3.client('s3')
bucket_name = 'blackboxlinkedcar'
timestamp = datetime.now()

# Generate the directory structure for the S3 object key
s3_prefix = timestamp.strftime('logfiles/%Y/%m/%d/%H/')

# Create the zipfiles directory if it doesn't exist
if not os.path.exists('zipfiles'):
    os.makedirs('zipfiles')

# Delete the previous log files
for filename in os.listdir('zipfiles'):
    os.remove(os.path.join('zipfiles', filename))
    print('old zipfiles successfully removed')

# Split each logfile into smaller parts and upload them individually
for filename in os.listdir('logfiles'):
    with open(os.path.join('logfiles', filename), 'rb') as f_in:
        file_size = os.path.getsize(os.path.join('logfiles', filename))
        print('Processing file {} ({} bytes)'.format(filename, file_size))

        # Split the logfile into chunks of 2MB (2,097,152 bytes)
        chunk_size = 2 * 1024 * 1024  # 2MB
        chunks = [chunk for chunk in iter(lambda: f_in.read(chunk_size), b'')]

        # Save the chunks to separate gzip files
        for i, chunk in enumerate(chunks):
            chunk_size = len(chunk)
            output_file = 'zipfiles/{}_{}_{}.gz'.format(timestamp.strftime('%Y_%m_%d_%H_%M_%S'), filename[:-4], i)
            logfile = '{}_{}_{}.gz'.format(timestamp.strftime('%Y_%m_%d_%H_%M_%S'), filename[:-4], i)

            # Create a new gzip file for the chunk data
            with gzip.open(output_file, 'wb', compresslevel=9) as f_out:
                # Write the chunk data to the output file
                f_out.write(chunk)
                print('Chunk {} ({} bytes) of file {} successfully zipped'.format(i, chunk_size, filename))

            # Upload the chunk to S3
            with open(output_file, 'rb') as data:
                s3.upload_fileobj(data, bucket_name, s3_prefix + logfile)
                print('Chunk {} ({} bytes) of file {} successfully uploaded to S3'.format(i, chunk_size, filename))

print('All logfiles successfully uploaded to S3')
