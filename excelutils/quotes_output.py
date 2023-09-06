from openpyxl.worksheet import worksheet
from openpyxl.styles import (NamedStyle, Font, Border, Side, PatternFill, Alignment)
from openpyxl.utils.cell import column_index_from_string

from settings import Catalog
from catalog import get_quote_numeric


def _get_quotes(catalog: Catalog = None,
                chapter: str = None, collection: str = None,
                section: str = None, subsection: str = None, table: str = None) -> list[str] | None:
    quote_codes = [code for code in catalog.quotes.keys()
                   if catalog.quotes[code].chapter == chapter and
                   catalog.quotes[code].collection == collection and
                   catalog.quotes[code].section == section and
                   catalog.quotes[code].subsection == subsection and
                   catalog.quotes[code].table == table
                   ]
    if len(quote_codes) > 0:
        return sorted(quote_codes, key=lambda x: get_quote_numeric(x))
    return None


def quotes_output(sheet: worksheet, catalog: Catalog, start_line: int,
                  chapter: str = None, collection: str = None,
                  section: str = None, subsection: str = None, table: str = None
                  ) -> bool:
    """ Записывает информацию из каталога о главах на лист sheet начиная со строки row. """
    quotes = _get_quotes(catalog, chapter, collection, section, subsection, table)
    if quotes:
        print(quotes)
        return True
    print(f"\tнет ни одной расценки")
    return False
