"""Tests for meme engine"""

import os
import shutil
import unittest
from pathlib import Path

from PIL import Image

from MemeEngine.engine import MemeEngine

PROJECT_ROOT = Path(__file__).parent.parent.resolve()


class TestMemeEngine(unittest.TestCase):
    """Test cases for MemeEngine."""

    def setUp(self):
        """Setup data for testing."""
        self.new_directory = './temp'
        self.wrong_directory = '../temp1'
        self.correct_image_path = os.path.join(PROJECT_ROOT, '_data', 'photos', 'dog', 'xander_1.jpg')
        self.incorrect_image_path = 'xander_1.jpg'

    def create_image(self, path: str, width: int = 500) -> Image:
        """Create image for testing."""
        meme_engine = MemeEngine(self.new_directory)
        return meme_engine.make_meme(path, "Quote Body", "The Great Me", width)

    def test_meme_engine_creation(self):
        """Test correct creation of meme engine."""
        MemeEngine(self.new_directory)
        MemeEngine(self.wrong_directory)
        MemeEngine(self.new_directory)

    def test_meme_creation(self):
        """Test successful meme creation using correct values."""
        image_path = self.create_image(self.correct_image_path)
        self.assertTrue(os.path.exists(image_path), 'Meme not saved')
        with Image.open(image_path) as image:
            self.assertTrue(image.width == 500)

    def test_meme_creation_wrong_image_path(self):
        """Test error on meme creation due to invalid image path."""
        try:
            self.create_image(self.incorrect_image_path)
        except FileNotFoundError:
            pass
        else:
            self.fail('No error given on meme creation for wrong input')

    def test_small_width(self):
        """Test image for width smaller than 500."""
        image_width = 200
        image_path = self.create_image(self.correct_image_path, width=image_width)
        with Image.open(image_path) as image:
            self.assertTrue(image.width == image_width)

    def test_big_width(self):
        """Test image for width bigger than 500."""
        image_width = 700
        image_path = self.create_image(self.correct_image_path, width=image_width)
        with Image.open(image_path) as image:
            self.assertTrue(image.width == 500)

    def test_float_width(self):
        """Test image for width bigger than 500."""
        image_width = 200.12
        self.create_image(self.correct_image_path, width=image_width)

    def tearDown(self):
        """Delete created directories."""
        try:
            shutil.rmtree(os.path.join(PROJECT_ROOT, 'temp'))
            shutil.rmtree(self.wrong_directory)
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    unittest.main()
