"""All logic required for ingesting quotes from different type of files."""

import os
import subprocess
import tempfile
from abc import ABC, abstractmethod

import docx
import pandas as pd

from .models import QuoteModel


class IngestorNotFoundError(Exception):
    """Error for unknown file types ingestors."""

    def __init__(self, msg):
        """Initialize parent constructor."""
        super().__init__(msg)


class PDFToTextNotFoundError(Exception):
    """Error for unknown file types ingestors."""

    def __init__(self, msg):
        """Initialize parent constructor."""
        super().__init__(msg)


class IngestorInterface(ABC):
    """Abstract class for implementing different ingestors."""

    extension = ''

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if ingestor supports the file type."""
        _, file_extension = os.path.splitext(path)
        return file_extension == cls.extension

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Parse data from file to a list of QuoteModels."""
        raise NotImplementedError


class TXTParser:
    """Parse quote models from txt files."""

    @staticmethod
    def _populate_quotes_from_txt(lines: list) -> list[QuoteModel]:
        quotes = []
        for line in lines:
            line = line.decode("utf-8") if type(line) is bytes else line
            line = line.split(' - ')
            if len(line) == 2:
                quotes.append(QuoteModel(*line))
        return quotes


class PDFIngestor(IngestorInterface, TXTParser):
    """Ingest quotes from .pdf files."""

    extension = '.pdf'

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Parse data from pdf file to a list of QuoteModels."""
        try:
            with tempfile.NamedTemporaryFile(suffix='.txt') as temp_txt_file:
                subprocess.run(("pdftotext", '-raw', path, temp_txt_file.name), check=True)
                lines = temp_txt_file.readlines()
                return cls._populate_quotes_from_txt(lines)
        except FileNotFoundError:
            raise PDFToTextNotFoundError('"pdftotext" is a required module, please install it before parsing pdf files.')


class TextIngestor(IngestorInterface, TXTParser):
    """Ingest quotes from .txt files."""

    extension = '.txt'

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Parse data from txt file to a list of QuoteModels."""
        with open(path, 'r') as txt_file:
            lines = txt_file.readlines()
            return cls._populate_quotes_from_txt(lines)


class CSVIngestor(IngestorInterface):
    """Ingest quotes from .csv files."""

    extension = '.csv'

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Parse data from csv file to a list of QuoteModels."""
        csv_rows = pd.read_csv(path)
        return [QuoteModel(row["body"], row["author"]) for _, row in csv_rows.iterrows()]


class DocxIngestor(IngestorInterface):
    """Ingest quotes from .docx files."""

    extension = '.docx'

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Parse data from docx file to a list of QuoteModels."""
        quotes = []
        doc = docx.Document(path)
        for paragraph in doc.paragraphs:
            try:
                body, author = paragraph.text.split(' - ')
            except ValueError:
                pass
            else:
                quotes.append(QuoteModel(body, author))
        return quotes


class Ingestor:
    """Ingestor to parse data in different types of files."""

    classes_mapping = {
        '.pdf': PDFIngestor,
        '.txt': TextIngestor,
        '.docx': DocxIngestor,
        '.csv': CSVIngestor,
    }

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Parse data from file path."""
        _, file_extension = os.path.splitext(path)
        try:
            class_instance = cls.classes_mapping[file_extension]()
        except KeyError:
            raise IngestorNotFoundError(f'Invalid file extension: {file_extension}')
        quotes = []
        try:
            if class_instance.can_ingest(path):
                quotes = class_instance.parse(path)
        except FileNotFoundError:
            raise FileNotFoundError(f'No such file or directory: {path}')
        except AttributeError:
            raise IngestorNotFoundError(f'No Ingestor found for file: {path}')
        return quotes

    @staticmethod
    def parse_quotes(file_paths: list) -> list[QuoteModel]:
        """Parse quotes from a list of files."""
        quotes = []
        for file_path in file_paths:
            quotes.extend(Ingestor.parse(file_path))
        return quotes
