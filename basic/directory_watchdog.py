#/usr/bin/env python

"""
Utility to watch a directory and copy new files.

Another solution would be rsync, but this is only a test, how to do it in
python. ;)
"""

import logging
import os.path
import shutil
import time
import hashlib

source_dir = r"\\190.9.220.10\data"
destination_dir = \
        r"C:\Documents and Settings\richard.poettler\Desktop\destination"
sleep_seconds = 30
# TODO: add already existing files to the set
done = set()
log_format = '%(asctime)s %(name)s: %(message)s'

logging.basicConfig(level=logging.INFO,
        format=log_format)
logger = logging.getLogger('watchdog')

# copy a logfile to the destination directory
logfile = os.path.join(destination_dir, "_copy.log")
if not os.path.isdir(os.path.dirname(logfile)):
    os.makedirs(os.path.dirname(logfile))
file_formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler(logfile)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def md5_for_file(filename):
    with open(filename) as fileobj:
        md5 = hashlib.md5()
        while True:
            content = fileobj.read(128) # md5 operates on 128 bit chunks
            if len(content) == 0:
                break
            md5.update(content)
    return md5.hexdigest()


logger.info("started watching")
while True:
    logger.debug("checking")
    # iterate over all directories in the source folder
    for dirpath, dirnames, filenames in os.walk(source_dir):
        actual_destination_dir = os.path.join(destination_dir,
                dirpath[len(source_dir):].strip(r'\/'))

        # iterate over all files in the source-sub-folder
        for filename in filenames:
            source_file = os.path.join(dirpath, filename)
            destination_file = os.path.join(actual_destination_dir, filename)
            md5sum = md5_for_file(source_file)

            # copy only, if the file wasn't already copied
            if md5sum not in done:
                logger.info("copy " + source_file)
                # create a new filename, if the actual one already exists
                counter = 1
                while os.path.isfile(destination_file):
                    base, extension = os.path.splitext(filename)
                    destination_file = os.path.join(actual_destination_dir,
                            base + "_" + str(counter) + extension)
                    counter += 1
                # create the output directory if needed
                if not os.path.isdir(os.path.dirname(destination_file)):
                    os.makedirs(os.path.dirname(destination_file))
                # copy the file and mark it as done
                shutil.copy(source_file, destination_file)
                done.add(md5sum)
    time.sleep(sleep_seconds)
