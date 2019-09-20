"""Module to copy files from one directory to another

The files are listed in a text file, one to a line

Script arguments:
    (Arguments given to this script if run from the command line)

    - source_dir -- The directory where the files currently live
    - dest_dir   -- The directory to where the files are to be copied
    - fname_file_list -- The path to the text file containing the
                            list of filenames to be copied

Note that these script arguments correspond precisely to the function arguments
"""
from shutil import copyfile 
import os.path
import sys
import traceback

def copy_files(source_dir, dest_dir, fname_file_list):
    """Copy files from one directory to another

    See module documentation for more information.
    Note that the function arguments align precisely with those to the module/script

    If a file is not found, the FileNotFound error will be caught
        and its stack trace printed
    """

    with open(fname_file_list, 'r') as f :
        for line in f:
            fname = line.strip()
            fsource = os.path.join( source_dir, fname )
            fdest = os.path.join( dest_dir, fname )
            try:
                copyfile( fsource, fdest )
            except FileNotFoundError as e:
                print("Caught error:")
                print(traceback.format_exc()) # print error stack trace


if __name__ == '__main__':

    ## set defaults
    source_dir = "/autograder/submission/"
    dest_dir   = "/autograder/source/"

    fname_file_list = "required_files.txt"
    
    ## check for command line arguments overriding defaults
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    if len(sys.argv) > 2:
        dest_dir = sys.argv[2]
    if len(sys.argv) > 3:
        fname_file_list = sys.argv[3]

    copy_files(source_dir, dest_dir, fname_file_list)
