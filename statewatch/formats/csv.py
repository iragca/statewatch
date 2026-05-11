from typing import List, Self, Any

from statewatch.db.models import Price


class CSV:
    """Format a sequence of objects as CSV text."""

    def __init__(self, data: Any, columns: list[str], separator: str = ","):
        """Initialize the CSV formatter.

        Parameters
        ----------
        data : Any
            Iterable of row objects to format.
        columns : list[str]
            Attribute names to include in the CSV output.
        separator : str, default=","
            Field separator to use between columns.
        """
        self.columns = columns
        self.separator = separator
        self.data = data

    @classmethod
    def from_price_list(cls, prices: List[Price], separator: str = ",") -> Self:
        """Create a CSV formatter for a list of Price objects.

        Parameters
        ----------
        prices : list[Price]
            List of Price rows to format.
        separator : str, default=","
            Field separator to use between columns.

        Returns
        -------
        Self
            A configured CSV instance for price data.
        """
        return cls(data=prices, columns=["date", "price"], separator=separator)

    def format(self) -> str:
        """Return the CSV document as a string.

        Returns
        -------
        str
            Formatted CSV text.
        """
        header = self._format_header()
        body_rows: list[str] = self._format_body()

        return header + "\n" + "\n".join(body_rows)

    def _format_header(self) -> str:
        """Format the CSV header row.

        Returns
        -------
        str
            Header row.
        """
        return self.separator.join(self.columns)

    def _format_body(self):
        """Format all data rows as CSV strings.

        Returns
        -------
        list[str]
            Formatted data rows.
        """
        return [self._format_row(row_data) for row_data in self.data]

    def _format_row(self, row_data: Any) -> str:
        """Format a single row object using the configured columns.

        Parameters
        ----------
        row_data : Any
            Row object to format.

        Returns
        -------
        str
            Formatted CSV row.
        """
        return self.separator.join(
            str(getattr(row_data, col_name)) for col_name in self.columns
        )

    def __str__(self) -> str:
        """Return the formatted CSV text.

        Returns
        -------
        str
            Formatted CSV text.
        """
        return self.format()
