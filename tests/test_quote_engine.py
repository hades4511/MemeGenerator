"""Tests for Quote Engine."""

import os
import unittest
from pathlib import Path

from QuoteEngine.ingestors import Ingestor, IngestorNotFoundError
from QuoteEngine.models import QuoteModel

PROJECT_ROOT = Path(__file__).parent.parent.resolve()


class TestQuoteMode(unittest.TestCase):
    """Test Quote Models."""

    def setUp(self):
        """Create test data."""
        self.body = "Quote Body"
        self.author = "The Great Me"

    def test_quote_model(self):
        """Test Successful Quote creation."""
        quote = QuoteModel(self.body, self.author)
        self.assertEqual(quote.body, self.body)
        self.assertEqual(quote.author, self.author)
        self.assertEqual(f'"{self.body}" - {self.author}', str(quote))


class TestIngestors(unittest.TestCase):
    """Test if ingestors as working properly."""

    def setUp(self):
        """Create test data."""
        data_path = os.path.join(PROJECT_ROOT, '_data', 'DogQuotes')
        self.correct_paths = {
            'pdf_file_path': os.path.join(data_path, 'DogQuotesPDF.pdf'),
            'txt_file_path': os.path.join(data_path, 'DogQuotesTXT.txt'),
            'docx_file_path': os.path.join(data_path, 'DogQuotesDOCX.docx'),
            'csv_file_path': os.path.join(data_path, 'DogQuotesCSV.csv'),
        }
        self.incorrect_file_format = os.path.join(data_path, 'DogQuotesCSV.abc')
        self.no_file_format = os.path.join(data_path, 'DogQuotesCSV')
        self.incorrect_file_path = 'DogQuotesCSV.csv'

    def test_all_ingestors_for_errors(self):
        """Test all ingestors when data is correct."""
        for file_path in self.correct_paths.values():
            self.assertTrue(type(Ingestor.parse(file_path)), list)

    def test_invalid_file_format(self):
        """Test exception raise on invalid file format."""
        try:
            Ingestor.parse(self.incorrect_file_format)
        except IngestorNotFoundError:
            pass
        else:
            self.fail('No exception raised for invalid file format.')

    def test_no_file_format(self):
        """Test exception raise on no file format."""
        try:
            Ingestor.parse(self.incorrect_file_format)
        except IngestorNotFoundError:
            pass
        else:
            self.fail('No exception raised for missing file format.')

    def test_incorrect_file_path(self):
        """Test exception raise on incorrect file path."""
        try:
            Ingestor.parse(self.incorrect_file_path)
        except FileNotFoundError:
            pass
        else:
            self.fail('No exception raised for incorrect file format.')


if __name__ == '__main__':
    unittest.main()
