import unittest
import os
from src.utils import validate_flac_file, create_output_directory, get_output_file_path

class TestUtils(unittest.TestCase):
    def test_validate_flac_file(self):
        self.assertFalse(validate_flac_file("test.mp3"))
        self.assertFalse(validate_flac_file("nonexistent.flac"))

    def test_get_output_file_path(self):
        input_path = "test.flac"
        output_dir = "output"
        expected = os.path.join(output_dir, "test.m4a")
        self.assertEqual(get_output_file_path(input_path, output_dir), expected)

    def test_create_output_directory(self):
        test_dir = "test_output"
        create_output_directory(test_dir)
        self.assertTrue(os.path.exists(test_dir))
        os.rmdir(test_dir)

if __name__ == '__main__':
    unittest.main()