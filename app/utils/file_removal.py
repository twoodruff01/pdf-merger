"""
Functions for cleaning out files from the server.
A bit hacky, but it works without using recursion :)
"""
import os
import glob
import time


# Remove all files in the loads directory, waiting 'cycle' amount of time between loops
# Be careful with calling this function and getting the paths right...
def file_cleaning(delete_cycle, upload_path, download_path, log):
    log.info('Initialising file_cleaning')
    while True:
        log.info('Setting timer for file_cleaning now')
        time.sleep(delete_cycle)
        log.info('Deleting loads')
        _clear_directory(upload_path)
        _clear_directory(download_path)


# Probably don't actually need this
def _less_files_than(max_file_number, path):
    number_of_files = 0
    with os.scandir(path=path) as iterator:
        for file in iterator:
            number_of_files += 1
            if number_of_files > max_file_number:
                return False
        return True


def _clear_directory(path):
    files = glob.glob(path + '/*')
    for file in files:
        os.remove(file)
