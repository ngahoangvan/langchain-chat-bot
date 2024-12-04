from unittest import TestCase
import os
from core.utils.common_utils import join_paths, calculate_token


class TestCommonUtils(TestCase):
    def test_join_paths(self):
        # Test joining two path components
        path1 = "folder1"
        path2 = "folder2"
        expected = os.path.join("folder1", "folder2")
        self.assertEqual(join_paths(path1, path2), expected)

        # Test joining multiple path components
        path3 = "file.txt"
        expected = os.path.join("folder1", "folder2", "file.txt")
        self.assertEqual(join_paths(path1, path2, path3), expected)

    def test_calculate_token(self):
        # Test empty string
        self.assertEqual(calculate_token(""), 0)

        # Test simple string
        text = "Hello, world!"
        self.assertTrue(calculate_token(text) > 0)

        # Test longer text
        long_text = "This is a longer text that should require more tokens to encode."
        self.assertTrue(calculate_token(long_text) > calculate_token(text))
