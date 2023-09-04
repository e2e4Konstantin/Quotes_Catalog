import re

from settings import catalog
from read_catalog import read_catalog


def catalog_none_check():
    collections = [(x.code, x.chapter) for x in catalog.collections.values() if x.chapter is None]
    print(f"Сборники с 0-ми главами: {len(collections)} -->", collections)

    sections = [(x.code, x.chapter, x.collection) for x in catalog.sections.values()
                if x.chapter is None or x.collection is None]
    print(f"Отделы с 0-ми главами или сборниками: {len(sections)} -->", sections)

    subsections = [(x.code, x.chapter, x.collection, x.section) for x in catalog.subsections.values()
                   if x.chapter is None or x.collection is None or x.section is None]
    print(f"Разделы с 0-ми главами или сборниками или отделами: {len(subsections)} -->", subsections)

    tables = [(x.code, x.chapter, x.collection, x.section, x.subsection) for x in catalog.tables.values()
              if x.chapter is None or x.collection is None or x.section is None or x.subsection is None]
    print(f"Таблицы с 0-ми главами или сборниками или отделами или разделами: {len(tables)} -->", tables)

    tables = [(x.code, x.chapter, x.collection, x.section, x.subsection) for x in catalog.tables.values()
              if x.chapter is None or x.collection is None]
    print(f"1. Таблицы с 0-ми главами или сборниками: {len(tables)} -->", tables)

    tables = [(x.code, x.chapter, x.collection, x.section, x.subsection) for x in catalog.tables.values()
              if x.section is None]
    print(f"2. Таблицы с 0-ми отделами: {len(tables)} -->", tables)

    tables = [(x.code, x.chapter, x.collection, x.section, x.subsection) for x in catalog.tables.values()
              if x.subsection is None]
    print(f"2. Таблицы с 0-ми разделами: {len(tables)} -->", tables)


def extract_int_code(code: str = None, target_name: str = '') -> int | None:
    """ Выделяет из входного кода целочисленное значение: главы, сборника, отдела, раздела """
    extract = None
    if code:
        match target_name:
            case 'chapter':
                extract = re.match(r"^\s*(\d+)", code)
                extract = extract.group(1).split('.', 1)[0] if extract else None
            case 'collection':
                extract = re.match(r"^\s*(\d+\.\d+)", code)
                extract = extract.group(1).split('.')[1].split('-', 1)[0] if extract else None
            case 'section':
                extract = re.match(r"^\s*(\d+\.\d+-\d+)", code)
                extract = extract.group(1).split('-', 2)[1] if extract else None
            case 'subsection':
                extract = re.match(r"^\s*(\d+\.\d+(-\d+){2})", code)
                extract = extract.group(1).split('-', 3)[2] if extract else None
            case _:
                return None
    return int(extract) if extract and isinstance(extract, str) and extract.isdigit() else None


def get_chapters() -> list[str] | None:
    chapter_codes = list(catalog.chapters.keys())
    if len(chapter_codes) > 0:
        chapter_codes.sort(key=lambda code: extract_int_code(code, 'chapter'))
        return chapter_codes
    return None


def get_collections(chapter: str = None) -> list[str] | None:
    collection_codes = [code for code in catalog.collections.keys() if catalog.collections[code].chapter == chapter]
    if len(collection_codes) > 0:
        collection_codes.sort(key=lambda code: extract_int_code(code, 'collection'))
        return collection_codes
    return None


def get_section(chapter: str = None, collection: str = None) -> list[str] | None:
    section_codes = [code for code in catalog.sections.keys()
                     if catalog.sections[code].chapter == chapter and catalog.sections[code].collection == collection]
    if len(section_codes) > 0:
        section_codes.sort(key=lambda code: extract_int_code(code, 'section'))
        return section_codes
    return None


def get_subsection(chapter: str = None, collection: str = None, section: str = None) -> list[str] | None:
    subsection_codes = [code for code in catalog.subsections.keys()
                        if catalog.subsections[code].chapter == chapter and
                        catalog.subsections[code].collection == collection and
                        catalog.subsections[code].section == section]
    if len(subsection_codes) > 0:
        subsection_codes.sort(key=lambda code: extract_int_code(code, 'subsection'))
        return subsection_codes
    return None


def get_selected_tables(selected_chapter: str | None = '',
                        selected_collection: str | None = '',
                        selected_section: str | None = '',
                        selected_subsection: str | None = '') -> list[str] | None:
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


def tables_out(chapter_code: str = None, collection_code: str = None,
               section_code: str = None, subsection_code: str = None, depth: int = 4) -> bool:
    """ Выводит в консоль Таблицы """
    tables = get_selected_tables(
        selected_chapter=chapter_code, selected_collection=collection_code,
        selected_section=section_code, selected_subsection=subsection_code
    )
    if tables:
        print("\t" * depth, f"таблицы ({len(tables)}): {tables}")
        return True
    # print("\t" * depth, f"таблиц нет")
    return False


def subsections_out(chapter_code: str = None, collection_code: str = None,
                    section_code: str = None, depth: int = 3) -> bool:
    """ Выводит в консоль Разделы """
    subsections = get_subsection(chapter=chapter_code, collection=collection_code, section=section_code)
    if subsections:
        print("\t" * depth, f"разделы ({len(subsections)}): {subsections}")
        for subsection in subsections:
            print("\t" * depth, f"{catalog.subsections[subsection].code!r} {catalog.subsections[subsection].title}")
            tables_out(chapter_code, collection_code, section_code, subsection, depth=depth + 1)
        return True
    # print("\t" * depth, f"разделов нет")
    return False


def sections_out(chapter_code: str = None, collection_code: str = None, depth: int = 2) -> bool:
    """ Выводит в консоль Разделы """
    sections = get_section(chapter=chapter_code, collection=collection_code)
    if sections:
        print("\t" * depth, f"отделы ({len(sections)}): {sections}")
        for section in sections:
            print("\t" * depth, f"{catalog.sections[section].code!r} {catalog.sections[section].title}")
            tables_out(chapter_code, collection_code, section)  # , depth=depth
            subsections_out(chapter_code, collection_code, section)
        return True
    # print("\t" * depth, f"отделов нет")
    return False


def collections_out(chapter_code: str = None, depth: int = 1) -> bool:
    """ Выводит в консоль Сборники """
    collections = get_collections(chapter=chapter_code)
    if collections:
        print("\t" * depth, f"сборники ({len(collections)}): {collections}")
        for collection in collections:
            print("\t" * depth, f"{catalog.collections[collection].code!r} {catalog.collections[collection].title}")
            tables_out(chapter_code, collection, depth=depth + 1)
            sections_out(chapter_code, collection)
        return True
    # print("\t" * depth, f"сборников нет")
    return False


def chapters_out(limit: int = 0) -> bool:
    """ Выводит в консоль Главы """
    chapters = get_chapters()
    if chapters:
        if 0 < limit <= len(chapters):
            chapters = chapters[: limit]
        print(f"главы ({len(chapters)}): {chapters}")
        for chapter in chapters:
            print(f"{catalog.chapters[chapter].code!r} {catalog.chapters[chapter].title}")
            tables_out(chapter, depth=0)
            collections_out(chapter)
        return True
    print(f"каталог пустой, нет ни одной Главы")
    return False


def application():
    path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\Quote_Catalog\src"
    # path = r"C:\Users\kazak.ke\PycharmProjects\Quotes_Catalog\src"
    file = r"catalog_3.xlsx"
    sheet = 'catalog'
    read_catalog(file, path, sheet)


if __name__ == "__main__":
    application()
    print(f"<< {'-' * 50} >>\n")
    catalog_none_check()
    print(f"<< {'-' * 50} >>\n")
    chapters_out(1)
