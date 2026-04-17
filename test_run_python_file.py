
import unittest
from config import *
from functions.run_python_file import run_python_file

class TestGetFilesInfo(unittest.TestCase):
    def test_main_file(self): 
        print("Result for 'main.py':")
        files_info = run_python_file("calculator", "main.py")
        print(files_info)

    def test_main_with_args_file(self): 
        print("Result for 'main.py with args':")
        files_info = run_python_file("calculator", "main.py", ["3 + 5"])
        print(files_info)

    def test_pkg_tests_file(self):
        print("Result for 'tests.py':")
        files_info = run_python_file("calculator", "tests.py")
        print(files_info)

    def test_for_error(self):
        print("Result for '../main.py':")
        files_info = run_python_file("calculator", "../main.py")
        print(files_info)

    def test_lorem_nonexistent_file(self): 
        print("Result for 'nonexiestnet.py':")
        files_info = run_python_file("calculator", "nonexistent.py")
        print(files_info)

    def test_lorem_error_file(self): 
        print("Result for 'lorem.txt':")
        files_info = run_python_file("calculator", "lorem.txt")
        print(files_info)

if __name__ == "__main__":
    unittest.main()
