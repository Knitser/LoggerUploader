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

# Zip and upload each logfile separately
for filename in os.listdir('logfiles'):
    output_file = 'zipfiles/{}_{}.gz'.format(timestamp.strftime('%Y_%m_%d_%H_%M_%S'), filename[:-4])
    logfile = '{}_{}.gz'.format(timestamp.strftime('%Y_%m_%d_%H_%M_%S'), filename[:-4])

    # Create a new gzip file for the output data
    with gzip.open(output_file, 'wb') as f_out:
        with open(os.path.join('logfiles', filename), 'rb') as f_in:
            # Read the input file and write its contents to the output file
            f_out.writelines(f_in)
            print('logfile successfully zipped')

    # Upload to S3
    with open(output_file, 'rb') as data:
        s3.upload_fileobj(data, bucket_name, s3_prefix + logfile)
        print('file successfully uploaded to S3')

print('All logfiles successfully uploaded to S3')
