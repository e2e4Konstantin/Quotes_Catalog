from openpyxl.worksheet import worksheet
from openpyxl.styles import Color, Font
from openpyxl.utils.cell import column_index_from_string

from settings import Catalog
from catalog import get_table_numeric
from excelutils.quotes_output import quotes_output
from openpyxl.styles import numbers


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


def _table_line_output(code: str, catalog: Catalog, sheet: worksheet, row: int) -> int:
    """ Записывает информацию из каталога о Таблице с шифром code на лист sheet в строку row. """
    table = catalog.tables[code]
    sheet.cell(row=row, column=column_index_from_string('A')).value = table.chapter
    sheet.cell(row=row, column=column_index_from_string('B')).value = table.collection
    sheet.cell(row=row, column=column_index_from_string('C')).value = table.section
    sheet.cell(row=row, column=column_index_from_string('D')).value = table.subsection
    sheet.cell(row=row, column=column_index_from_string('E')).value = table.code
    sheet.cell(row=row, column=column_index_from_string('G')).value = table.title
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    for column in columns:
        sheet.cell(row=row, column=column_index_from_string(column)).style = 'table_name'
        sheet.cell(row=row, column=column_index_from_string(column)).number_format = numbers.FORMAT_TEXT
    # sheet.cell(row=row, column=column_index_from_string('F')).font = Font(
    #         name='Calibri', color=Color(rgb='000000'), size=8, bold=False)
    return row+1



def tables_output(sheet: worksheet, catalog: Catalog, start_line: int,
                  chapter: str = None, collection: str = None,
                  section: str = None, subsection: str = None) -> int:
    """ Записывает информацию из каталога о таблицах на лист sheet начиная со строки start_line. """
    tables = _get_tables(catalog, chapter, collection, section, subsection)
    if tables:
        print('\t\t таблицы: ',tables)
        row = start_line
        for table in tables:
            row = _table_line_output(table, catalog, sheet, row)
            row = quotes_output(sheet, catalog, row, chapter, collection, section, subsection, table)
        return row
    print(f"\tнет ни одной таблицы")
    return start_line
