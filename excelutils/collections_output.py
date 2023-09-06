from openpyxl.worksheet import worksheet
from openpyxl.styles import (NamedStyle, Font, Border, Side, PatternFill, Alignment)
from openpyxl.utils.cell import column_index_from_string

from settings import Catalog
from catalog import get_collection_numeric
from excelutils.quotes_output import quotes_output
from excelutils.tables_output import tables_output



def _get_collection(catalog: Catalog = None, chapter: str = None) -> list[str] | None:
    """ Формирует список шифров сборников для указанной главы. """
    collection_codes = [code for code in catalog.collections.keys()
                        if catalog.collections[code].chapter == chapter]
    if len(collection_codes) > 0:
        return sorted(collection_codes, key=lambda x: get_collection_numeric(x))
    return None


def collection_output(sheet: worksheet, catalog: Catalog, start_line: int, chapter: str = None) -> bool:
    """ Записывает информацию из каталога о сборниках на лист sheet начиная со строки start_line. """
    collections = _get_collection(catalog, chapter)
    if collections:
        for collection in collections:
            print('\t', catalog.collections[collection].code, catalog.collections[collection].title)
            current_row = quotes_output(sheet, catalog, start_line, chapter=chapter, collection=collection)
            current_row = tables_output(sheet, catalog, current_row + 1, chapter=chapter, collection=collection)
        return True
    print(f"\tнет ни одного сборника")
    return False
