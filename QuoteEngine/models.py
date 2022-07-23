"""File containing all models required for quotes."""


class QuoteModel:
    """A model class for quotes."""

    def __init__(self, quote: str, author: str):
        """Initialize parameters."""
        self.body = self.normalize_str(quote)
        self.author = self.normalize_str(author)

    @staticmethod
    def normalize_str(string: str) -> str:
        """Normalize strings."""
        return string.rstrip().replace('"', '')

    def __str__(self):
        """Represent QuoteModel in string form."""
        return f'"{self.body}" - {self.author}'

    def __repr__(self):
        """Machine representation of QuoteModel."""
        return self.__str__()
