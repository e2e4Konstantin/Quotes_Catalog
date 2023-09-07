from openpyxl.worksheet import worksheet
from openpyxl.styles import Font, Color
from openpyxl.utils.cell import column_index_from_string
from openpyxl.styles import numbers

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


def _quote_line_output(code: str, catalog: Catalog, sheet: worksheet, row: int) -> int:
    """ Записывает информацию из каталога о Расценке с шифром code на лист sheet в строку row. """
    quote = catalog.quotes[code]
    sheet.cell(row=row, column=column_index_from_string('A')).value = quote.chapter
    sheet.cell(row=row, column=column_index_from_string('B')).value = quote.collection
    sheet.cell(row=row, column=column_index_from_string('C')).value = quote.section
    sheet.cell(row=row, column=column_index_from_string('D')).value = quote.subsection
    sheet.cell(row=row, column=column_index_from_string('E')).value = quote.table
    sheet.cell(row=row, column=column_index_from_string('F')).value = quote.code
    sheet.cell(row=row, column=column_index_from_string('G')).value = quote.title
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    for column in columns:
        sheet.cell(row=row, column=column_index_from_string(column)).style = 'quote_line'
        sheet.cell(row=row, column=column_index_from_string(column)).number_format = numbers.FORMAT_TEXT
    sheet.cell(row=row, column=column_index_from_string('F')).font = Font(
            name='Calibri', color=Color(rgb='34495E'), size=8, bold=True)
    return row+1


def quotes_output(sheet: worksheet, catalog: Catalog, start_line: int,
                  chapter: str = None, collection: str = None,
                  section: str = None, subsection: str = None, table: str = None
                  ) -> int:
    """ Записывает информацию из каталога о главах на лист sheet начиная со строки row. """
    quotes = _get_quotes(catalog, chapter, collection, section, subsection, table)
    if quotes:
        print('\t\t', quotes)
        row = start_line
        for quote in quotes:
            row = _quote_line_output(quote, catalog, sheet, row)
        return row
    print(f"\tнет ни одной расценки")
    return start_line
