
import unittest
from config import *
from functions.write_file import write_file

class TestGetFilesInfo(unittest.TestCase):
    def test_lorem_file(self): 
        print("Result for 'lorem.txt':")
        files_info = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(files_info)

    def test_write_lorem(self): 
        print("Result for 'pkg/morelorem.txt':")
        files_info = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(files_info)

    def test_for_error(self):
        print("Result for '/tmp/temp.txt':")
        files_info = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(files_info)

if __name__ == "__main__":
    unittest.main()
