from openpyxl.worksheet import worksheet
from openpyxl.styles import (NamedStyle, Font, Border, Side, PatternFill, Alignment)
from openpyxl.utils.cell import column_index_from_string
from settings import Catalog
from catalog import extract_int_code

from excelutils.quotes_output import quotes_output
from excelutils.tables_output import tables_output
from excelutils.collections_output import collection_output


def _get_chapters(catalog: Catalog = None) -> list[str] | None:
    """ Готовит список глав из каталога и сортирует его по номеру главы """
    chapter_codes = list(catalog.chapters.keys())
    if len(chapter_codes) > 0:
        chapter_codes.sort(key=lambda code: extract_int_code(code, 'chapter'))
        return chapter_codes
    return None


def _range_decorating(sheet: worksheet, row, columns: list[str], style_name: str):
    """ Устанавливает стиль style_name для ячеек из списка columns """
    for column in columns:
        sheet.cell(row=row, column=column_index_from_string(column)).style = style_name


def chapter_line_output(code: str, catalog: Catalog, sheet: worksheet, row: int):
    """ Записывает информацию из каталога о главе code на лист sheet в строку row """
    chapter = catalog.chapters[code]
    sheet.cell(row=row, column=column_index_from_string('A')).value = chapter.code
    sheet.cell(row=row, column=column_index_from_string('G')).value = chapter.title
    _range_decorating(sheet, row, ['A', 'B', 'C', 'D', 'E', 'F', 'G'], 'chapter_line')


def chapters_output(sheet: worksheet, catalog: Catalog, start_line: int, limit: int = 0) -> bool:
    """ Записывает информацию из каталога о главах на лист sheet начиная со строки row. """
    chapters = _get_chapters(catalog)
    if chapters:
        if 0 < limit <= len(chapters):
            chapters = chapters[: limit]
        print(f"главы ({len(chapters)}): {chapters}")
        row = start_line
        for chapter in chapters:
            chapter_line_output(chapter, catalog, sheet, row)
            print(f"{catalog.chapters[chapter].code!r} {catalog.chapters[chapter].title}")
            current_row = quotes_output(sheet, catalog, row, chapter=chapter)
            current_row = tables_output(sheet, catalog, current_row+1, chapter=chapter)
            current_row = collection_output(sheet, catalog, current_row+1, chapter=chapter)
            row = current_row + 1
        return True
    print(f"нет ни одной Главы")
    return False
