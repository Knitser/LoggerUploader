
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
    for chunk_filename, chunk_data in logfile_splitter.split_logfile(input_path):
        s3_uploader.upload_chunk(chunk_data, chunk_filename)

print('All logfiles successfully uploaded to S3')