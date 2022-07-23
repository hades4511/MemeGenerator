"""Engine used for generating memes using quotes."""

import os
from tempfile import NamedTemporaryFile

from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """Create meme from given parameters."""

    font = './_data/fonts/Raleway-Light.ttf'

    def __init__(self, directory_path: str):
        """Create save directory."""
        self.directory_path = directory_path
        os.makedirs(directory_path, exist_ok=True)

    def _write_quote(self, text: str, author: str, image: Image):
        """Write quote on image."""
        drawn_image = ImageDraw.Draw(image)
        quote = f'"{text}" - {author}'
        drawn_image.text((5, int(image.height/2)), quote, font=ImageFont.truetype(self.font, 20))

    @staticmethod
    def _resize_image(image: Image, width: int = 500):
        """Resize image to a max of 500."""
        resized_width = 500 if width > 500 else width
        if image.width <= resized_width:
            return image
        return image.resize((int(resized_width), int((image.height / image.width) * resized_width)))

    def make_meme(self, img_path: str, text: str, author: str, width: int = 500) -> str:
        """Make meme from given data."""
        try:
            with Image.open(img_path) as image:
                resized_image = self._resize_image(image, width)
                self._write_quote(text, author, resized_image)
                temp_file = NamedTemporaryFile(dir=self.directory_path, prefix='meme_', suffix='.jpg', delete=False)
                resized_image.save(temp_file)
                return temp_file.name
        except FileNotFoundError:
            raise FileNotFoundError(f'Image file provided does not exist. file path:{img_path}')
