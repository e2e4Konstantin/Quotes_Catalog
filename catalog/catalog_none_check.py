from settings import Catalog


def catalog_none_check(catalog: Catalog = None):
    """ Выводит позиции у которых в коде есть нулевые родители """
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