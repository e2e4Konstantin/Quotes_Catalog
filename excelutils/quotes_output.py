from openpyxl.worksheet import worksheet
from openpyxl.utils.cell import column_index_from_string
from openpyxl.styles import numbers

from settings import Catalog, items_fonts, item_index
from catalog import get_numeric_stamp


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
    # группировка 6
    group_number = item_index['quote'] + 1
    sheet.row_dimensions.group(row, row + 1, outline_level=group_number)
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    for column in columns:
        sheet.cell(row=row, column=column_index_from_string(column)).style = 'quote_line'
        sheet.cell(row=row, column=column_index_from_string(column)).font = items_fonts[item_index['quote']]
        sheet.cell(row=row, column=column_index_from_string(column)).number_format = numbers.FORMAT_TEXT
    return row+1


def _get_quotes(catalog: Catalog = None,
                chapter: str = None, collection: str = None,
                section: str = None, subsection: str = None, table: str = None) -> list[str] | None:
    """ Создает список шифров расценок и сортирует его. """
    tmp = catalog.quotes.keys()
    quote_codes = []
    for code in tmp:
        quote = catalog.quotes[code]
        if quote.chapter == chapter:
            if quote.collection == collection:
                if quote.section == section:
                    if quote.subsection == subsection:
                        if quote.table == table:
                            quote_codes.append(code)
    # quote_codes = [code for code in catalog.quotes.keys()
    #                if catalog.quotes[code].chapter == chapter and
    #                catalog.quotes[code].collection == collection and
    #                catalog.quotes[code].section == section and
    #                catalog.quotes[code].subsection == subsection and
    #                catalog.quotes[code].table == table
    #                ]
    if len(quote_codes) > 0:
        return sorted(quote_codes, key=lambda x: tuple(map(int, get_numeric_stamp(x, 'quote'))))
    return None


def quotes_output(sheet: worksheet, catalog: Catalog, start_line: int,
                  chapter: str = None, collection: str = None,
                  section: str = None, subsection: str = None, table: str = None
                  ) -> int:
    """ Записывает информацию о Расценках из catalog на лист sheet на строку row. """
    quotes = _get_quotes(catalog, chapter, collection, section, subsection, table)
    if quotes:
        row = start_line
        for quote in quotes:
            # print('\t\t\t\t\t', f"{catalog.quotes[quote].code!r} {catalog.quotes[quote].title}")
            row = _quote_line_output(quote, catalog, sheet, row)
        return row
    # print(f"\t\t\t\t\tнет ни одной расценки")
    return start_line
