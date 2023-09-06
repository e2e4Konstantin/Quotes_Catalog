from settings import Catalog
from catalog.read_catalog import catalog_fill
from catalog.extract_code import extract_int_code
from catalog.get_selected_tables import get_selected_tables


def catalog_none_check(catalog: Catalog = None):
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


def get_chapters(catalog: Catalog = None) -> list[str] | None:
    chapter_codes = list(catalog.chapters.keys())
    if len(chapter_codes) > 0:
        chapter_codes.sort(key=lambda code: extract_int_code(code, 'chapter'))
        return chapter_codes
    return None


def get_collections(catalog: Catalog = None, chapter: str = None) -> list[str] | None:
    collection_codes = [code for code in catalog.collections.keys() if catalog.collections[code].chapter == chapter]
    if len(collection_codes) > 0:
        collection_codes.sort(key=lambda code: extract_int_code(code, 'collection'))
        return collection_codes
    return None


def get_section(catalog: Catalog = None, chapter: str = None, collection: str = None) -> list[str] | None:
    section_codes = [code for code in catalog.sections.keys()
                     if catalog.sections[code].chapter == chapter and catalog.sections[code].collection == collection]
    if len(section_codes) > 0:
        section_codes.sort(key=lambda code: extract_int_code(code, 'section'))
        return section_codes
    return None


def get_subsection(catalog: Catalog = None, chapter: str = None, collection: str = None, section: str = None) -> list[str] | None:
    subsection_codes = [code for code in catalog.subsections.keys()
                        if catalog.subsections[code].chapter == chapter and
                        catalog.subsections[code].collection == collection and
                        catalog.subsections[code].section == section]
    if len(subsection_codes) > 0:
        subsection_codes.sort(key=lambda code: extract_int_code(code, 'subsection'))
        return subsection_codes
    return None



def tables_out(catalog: Catalog = None, chapter_code: str = None, collection_code: str = None,
               section_code: str = None, subsection_code: str = None, depth: int = 4) -> bool:
    """ Выводит в консоль Таблицы """
    tables = get_selected_tables(
        catalog,
        selected_chapter=chapter_code, selected_collection=collection_code,
        selected_section=section_code, selected_subsection=subsection_code
    )
    if tables:
        print("\t" * depth, f"таблицы ({len(tables)}): {tables}")
        return True
    # print("\t" * depth, f"таблиц нет")
    return False


def subsections_out(catalog: Catalog = None, chapter_code: str = None, collection_code: str = None,
                    section_code: str = None, depth: int = 3) -> bool:
    """ Выводит в консоль Разделы """
    subsections = get_subsection(catalog, chapter=chapter_code, collection=collection_code, section=section_code)
    if subsections:
        print("\t" * depth, f"разделы ({len(subsections)}): {subsections}")
        for subsection in subsections:
            print("\t" * depth, f"{catalog.subsections[subsection].code!r} {catalog.subsections[subsection].title}")
            tables_out(catalog, chapter_code, collection_code, section_code, subsection, depth=depth + 1)
        return True
    # print("\t" * depth, f"разделов нет")
    return False


def sections_out(catalog: Catalog = None, chapter_code: str = None, collection_code: str = None, depth: int = 2) -> bool:
    """ Выводит в консоль Разделы """
    sections = get_section(catalog, chapter=chapter_code, collection=collection_code)
    if sections:
        print("\t" * depth, f"отделы ({len(sections)}): {sections}")
        for section in sections:
            print("\t" * depth, f"{catalog.sections[section].code!r} {catalog.sections[section].title}")
            tables_out(catalog, chapter_code, collection_code, section)  # , depth=depth
            subsections_out(catalog, chapter_code, collection_code, section)
        return True
    # print("\t" * depth, f"отделов нет")
    return False


def collections_out(catalog: Catalog = None, chapter_code: str = None, depth: int = 1) -> bool:
    """ Выводит в консоль Сборники """
    collections = get_collections(catalog, chapter=chapter_code)
    if collections:
        print("\t" * depth, f"сборники ({len(collections)}): {collections}")
        for collection in collections:
            print("\t" * depth, f"{catalog.collections[collection].code!r} {catalog.collections[collection].title}")
            tables_out(catalog, chapter_code, collection, depth=depth + 1)
            sections_out(catalog, chapter_code, collection)
        return True
    # print("\t" * depth, f"сборников нет")
    return False


def chapters_out(catalog: Catalog = None, limit: int = 0) -> bool:
    """ Выводит в консоль Главы из catalog """
    chapters = get_chapters(catalog)
    if chapters:
        if 0 < limit <= len(chapters):
            chapters = chapters[: limit]
        print(f"главы ({len(chapters)}): {chapters}")
        for chapter in chapters:
            print(f"{catalog.chapters[chapter].code!r} {catalog.chapters[chapter].title}")
            tables_out(catalog, chapter, depth=0)
            collections_out(catalog, chapter)
        return True
    print(f"каталог пустой, нет ни одной Главы")
    return False





if __name__ == "__main__":
    stor = catalog_fill()
    stor.info()
    print(f"<< {'-' * 50} >>\n")
    catalog_none_check(stor)
    print(f"<< {'-' * 50} >>\n")
    chapters_out(stor, 1)
