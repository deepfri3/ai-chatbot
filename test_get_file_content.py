
import unittest
from config import MAX_CHARS
from functions.get_file_content import get_file_content

class TestGetFilesInfo(unittest.TestCase):
    def test_lorem_file(self): 
        files_info = get_file_content("calculator", "lorem.txt")
        print("Result for 'lorem.txt':")
        truncation_message = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
        if truncation_message in files_info:
            print(f"Truncated at {MAX_CHARS}")
        print(f'Length of content: {len(files_info)}')

    def test_main_file(self): 
        files_info = get_file_content("calculator", "main.py")
        print("Result for 'main.py':")
        print(files_info)

    def test_pkg_calculator_file(self):
        files_info = get_file_content("calculator", "pkg/calculator.py")
        print("Result for 'pkg/calculator.py':")
        print(files_info)

    def test_bin_slash_cat_file(self):
        files_info = get_file_content("calculator", "/bin/cat")
        print("Result for '/bin/cat':")
        print(files_info)

    def test_for_error(self):
        files_info = get_file_content("calculator", "pkg/does_not_exist.py")
        print("Result for 'pkg/does_not_exist.py':")
        print(files_info)

if __name__ == "__main__":
    unittest.main()
