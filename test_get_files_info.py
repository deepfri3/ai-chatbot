
import unittest
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_current_directory(self): 
        files_info = get_files_info("calculator", ".")
        print("Result for current directory:")
        print(files_info)

    def test_pkg_directory(self):
        files_info = get_files_info("calculator", "pkg")
        print("Result for 'pkg' directory:")
        print(files_info)

    def test_bin_directory(self):
        files_info = get_files_info("calculator", "/bin")
        print("Result for '/bin' directory:")
        print(files_info)

    def test_for_error(self):
        files_info = get_files_info("calculator", "../")
        print("Result for '../' directory:")
        print(files_info)

if __name__ == "__main__":
    unittest.main()
