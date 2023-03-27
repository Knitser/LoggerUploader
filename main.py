from datetime import datetime
from upload_s3 import LogfileSplitter, S3Uploader
import os
import subprocess

subprocess.run(['pip', 'install', '-r', 'requirements.txt'])


def main():
    # changing variables
    file_format = datetime.now().strftime('logfiles/%Y/%m/%d/%H/')
    chunk_size_2mb = 2 * 1024 * 1024

    s3_uploader = S3Uploader('blackboxlinkedcar', file_format)
    logfile_splitter = LogfileSplitter(chunk_size_2mb)

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
