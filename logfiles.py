import boto3
import gzip
import os
from datetime import datetime

s3 = boto3.client('s3')
bucket_name = 'blackboxlinkedcar'
timestamp = datetime.now()

# Generate the directory structure for the S3 object key
s3_prefix = timestamp.strftime('logfiles/%Y/%m/%d/%H/')

output_file = 'zipfiles/{}_logfile.gz'.format(timestamp.strftime('%Y_%m_%d_%H_%M_%S'))
logfile = '{}_logfile.gz'.format(timestamp.strftime('%Y_%m_%d_%H_%M_%S'))

# Delete the previous log files
for filename in os.listdir('zipfiles'):
    os.remove(os.path.join('zipfiles', filename))
    print('old zipfiles successfully removed')

# Create a new gzip file for the output data
with gzip.open(output_file, 'wb', compresslevel=9) as f_out:
    # This will append all files into 1 zip file.
    for filename in os.listdir('logfiles'):
        filepath = os.path.join('logfiles', filename)
        with open(filepath, 'rb') as f_in:
            # Read the input file and write its contents to the output file
            f_out.writelines(f_in)
            print('logfile successfully zipped')

# Upload to S3
with open(output_file, 'rb') as data:
    s3.upload_fileobj(data, bucket_name, s3_prefix + logfile)
    print('file successfully uploaded to S3')
