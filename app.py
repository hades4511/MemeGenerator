"""Flask app for meme generator."""

import glob
import mimetypes
import os
import random
from pathlib import Path
from tempfile import NamedTemporaryFile

import requests
from flask import Flask, render_template, request
from PIL import UnidentifiedImageError

from MemeEngine.engine import MemeEngine
from QuoteEngine.ingestors import Ingestor

app = Flask(__name__)
ROOT_DIR = Path(__file__).parent.resolve()
meme = MemeEngine('./static')


def setup():
    """Load all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = Ingestor.parse_quotes(quote_files)
    images_path = "./_data/photos/dog/"
    imgs = glob.glob(f'{images_path}/*.jpg')

    return quotes, imgs


def create_static_path(image_path: str) -> Path:
    """Create static path from absolute path."""
    return Path(image_path).relative_to(ROOT_DIR)


def save_image_from_url(image_url: str) -> str:
    """Create image from URL and return its extension."""
    response = requests.get(image_url, allow_redirects=True)
    extension = mimetypes.guess_extension(response.headers["content-type"])
    if not extension:
        raise Exception(f'Invalid URL for image: {image_url}')
    with NamedTemporaryFile(suffix=extension, delete=False) as url_image:
        url_image.write(response.content)
        return url_image.name


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=create_static_path(path))


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    quote_body = request.form.get('body')
    quote_author = request.form.get('author')

    try:
        url_image_path = save_image_from_url(request.form.get('image_url'))
        path = meme.make_meme(url_image_path, quote_body, quote_author)
    except requests.exceptions.ConnectionError:
        return render_template('error.html', msg='Invalid URL provided.')
    except UnidentifiedImageError:
        return render_template('error.html', msg='Invalid image type provided.')

    os.remove(url_image_path)
    return render_template('meme.html', path=create_static_path(path))


if __name__ == "__main__":
    app.run()
