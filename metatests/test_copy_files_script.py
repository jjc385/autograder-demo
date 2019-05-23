from copy_files import copy_files
import unittest
import os
import sys

class TestCopyFiles(unittest.TestCase):
    """Test the script used to copy required files"""

    def setUp(self):
        self.path = "metatests/test_files/"
        self.fname1 = "dummyfile1.txt"
        self.fname2 = "dummyfile2.txt"
        self.fname_missing = "dummyfile_missing.txt"

        self.dest_dir = self.path+"file_copy_dest_dir"
        os.makedirs(self.dest_dir, exist_ok=True)
        self.assertTrue(os.path.isdir(self.dest_dir))

        ## ensure the destination directory is empty
        for dirpath, dirnames, files in os.walk(self.dest_dir):
            self.assertEqual(len(files), 0)
            break

        self.fname_filelist = self.path+"file_list.txt"  ## will be created during tests


    def test_simple(self):
        with open(self.fname_filelist, 'w') as f:
            print(self.fname1, file=f)
            print(self.fname2, file=f)

        copy_files(self.path, self.dest_dir, self.fname_filelist)
        self.assertTrue(os.path.isfile(self.path+self.fname1))
        self.assertTrue(os.path.isfile(self.path+self.fname2))


    def test_missing(self):
        with open(self.fname_filelist, 'w') as f:
            print(self.fname1, file=f)
            print(self.fname_missing, file=f)
            print(self.fname2, file=f)

        ## suppress output
        sys.stdout = None
        copy_files(self.path, self.dest_dir, self.fname_filelist)
        sys.stdout = sys.__stdout__
        self.assertTrue(os.path.isfile(self.path+self.fname1))
        self.assertFalse(os.path.isfile(self.path+self.fname_missing))
        self.assertTrue(os.path.isfile(self.path+self.fname2))

    def tearDown(self):
        ## remove all files in the destination directory
        for dirpath, dirnames, files in os.walk(self.dest_dir):
            for f in files:
                os.remove(os.path.join(self.dest_dir,f))
            break
        
        os.remove(self.fname_filelist)
