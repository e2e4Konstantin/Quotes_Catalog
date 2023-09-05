from settings import Catalog
from catalog.extract_int_code import extract_int_code


def get_selected_tables(catalog: Catalog = None, selected_chapter: str | None = '',
                        selected_collection: str | None = '',
                        selected_section: str | None = '',
                        selected_subsection: str | None = '') -> list[str] | None:
    """ Выбор таблиц из catalog по условиям. """
    table_codes = []
    check = lambda x: x == ''
    if not check(selected_chapter) and check(selected_collection) and check(selected_section) and check(
            selected_subsection):
        # print(f"глава: {selected_chapter!r}")
        table_codes = [code for code in catalog.tables.keys() if catalog.tables[code].chapter == selected_chapter]
        table_codes.sort(key=lambda code: extract_int_code(code, 'chapter'))
    else:
        if not check(selected_chapter) and not check(selected_collection) and check(selected_section) and check(
                selected_subsection):
            # print(f"глава & сборник: {selected_chapter!r} & {selected_collection!r}")
            table_codes = [code for code in catalog.tables.keys()
                           if catalog.tables[code].chapter == selected_chapter and catalog.tables[
                               code].collection == selected_collection]
            table_codes.sort(key=lambda code: extract_int_code(code, 'collection'))
        else:
            if not check(selected_chapter) and not check(selected_collection) and not check(selected_section) and check(
                    selected_subsection):
                # print(f"глава & сборник & отдел: {selected_chapter!r} & {selected_collection!r} & {selected_section!r}")
                table_codes = [code for code in catalog.tables.keys()
                               if catalog.tables[code].chapter == selected_chapter and
                               catalog.tables[code].collection == selected_collection and
                               catalog.tables[code].section == selected_section
                               ]
                table_codes.sort(key=lambda code: extract_int_code(code, 'section'))
            else:
                if not check(selected_chapter) and not check(selected_collection) and not check(
                        selected_section) and not check(selected_subsection):
                    # print(f"глава & сборник & отдел & раздел: {selected_chapter!r} & {selected_collection!r} & {selected_section!r} & {selected_subsection!r}")
                    table_codes = [code for code in catalog.tables.keys()
                                   if catalog.tables[code].chapter == selected_chapter and
                                   catalog.tables[code].collection == selected_collection and
                                   catalog.tables[code].section == selected_section and
                                   catalog.tables[code].subsection == selected_subsection
                                   ]
                    table_codes.sort(key=lambda code: extract_int_code(code, 'subsection'))
    return table_codes if len(table_codes) > 0 else None
