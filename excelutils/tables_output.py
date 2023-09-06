from openpyxl.worksheet import worksheet
from openpyxl.styles import (NamedStyle, Font, Border, Side, PatternFill, Alignment)
from openpyxl.utils.cell import column_index_from_string

from settings import Catalog
from catalog import get_table_numeric
from excelutils.quotes_output import quotes_output


def _get_tables(catalog: Catalog = None,
                chapter: str = None, collection: str = None,
                section: str = None, subsection: str = None) -> list[str] | None:
    table_codes = [code for code in catalog.tables.keys()
                   if catalog.tables[code].chapter == chapter and
                   catalog.tables[code].collection == collection and
                   catalog.tables[code].section == section and
                   catalog.tables[code].subsection == subsection
                   ]
    if len(table_codes) > 0:
        return sorted(table_codes, key=lambda x: get_table_numeric(x))
    return None


def tables_output(sheet: worksheet, catalog: Catalog, start_line: int,
                  chapter: str = None, collection: str = None,
                  section: str = None, subsection: str = None) -> bool:
    """ Записывает информацию из каталога о таблицах на лист sheet начиная со строки start_line. """
    tables = _get_tables(catalog, chapter, collection, section, subsection)
    if tables:
        print(tables)
        quotes_output(sheet, catalog, start_line, chapter, collection, section, subsection, tables[0])
        return True
    print(f"\tнет ни одной таблицы")
    return False
