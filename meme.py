"""Main file to parse arguments and generate memes."""

import os
import random
from argparse import ArgumentParser
from pathlib import Path

from MemeEngine.engine import MemeEngine
from QuoteEngine.ingestors import Ingestor
from QuoteEngine.models import QuoteModel


def generate_meme(path: Path = None, body: str = None, author: str = None) -> str:
    """Generate a meme given an path and a quote."""
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = Ingestor.parse_quotes(quote_files)

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


def create_arg_parser() -> ArgumentParser:
    """Create an Argument Parser.

    The parser should allow the following optional commands:
        --body:     Quote Body
        --author:   Quote Author
        --path:     Image path for meme generation

    :return: A tuple of the top-level, inspect, and query parsers.
    """
    arg_parser = ArgumentParser(
        description="Create Meme using quotes."
    )

    arg_parser.add_argument('--body', type=str)
    arg_parser.add_argument('--author', type=str)
    arg_parser.add_argument('--path', type=Path)

    return arg_parser


if __name__ == "__main__":
    parser = create_arg_parser()
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
