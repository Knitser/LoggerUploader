import os
from datetime import datetime
import gzip


class LogfileSplitter:
    def __init__(self, file_size):
        self.file_size = file_size

    def split_logfile(self, input_path):
        with open(input_path, 'rb') as f_in:
            file_size = os.path.getsize(input_path)
            print(f'Processing file {input_path} ({file_size} bytes)')

            # Split the logfile into chunks of 2mb, defined in the main.py file.
            chunks = [chunk for chunk in iter(lambda: f_in.read(self.file_size), b'')]

            # Save the chunks to separate gzip files
            for i, chunk in enumerate(chunks):
                file_size = len(chunk)
                filename = os.path.splitext(os.path.basename(input_path))[0]
                timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                output_path = f'zipfiles/{timestamp}_{filename}_{i}.gz'

                # Create a new gzip file for the chunk data
                with gzip.open(output_path, 'wb', compresslevel=9) as f_out:
                    # Write the chunk data to the output file
                    f_out.write(chunk)
                    print(f'Chunk {i} ({file_size} bytes) of file {input_path} successfully zipped')

                # Yield the chunk filename for uploading to S3
                yield output_path
