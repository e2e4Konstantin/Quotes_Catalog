import re

from settings import catalog
from read_catalog import read_catalog
import random


def application():
    path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\Quote_Catalog\src"
    # path = r"C:\Users\kazak.ke\PycharmProjects\Quotes_Catalog\src"
    file = r"catalog_3.xlsx"
    sheet = 'catalog'
    read_catalog(file, path, sheet)


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





#
# table_0 = [catalog.tables[i].code for i in catalog.tables.keys()]
# print(len(table_0))
# table_1 = [catalog.tables[i].code for i in catalog.tables.keys() if catalog.tables[i].chapter == '3']
# print(len(table_1))
# table_2 = [x.code for x in catalog.tables.values() if x.chapter == '3' and x.collection is None]
# print('collection', len(table_2), table_2[:5], '.....')
#
# table_3 = [x.code for x in catalog.tables.values() if x.chapter == '3' and x.section is None]
# print('section', len(table_3), table_3[:5], '.....')
#
# table_4 = [x.code for x in catalog.tables.values() if x.chapter == '3' and x.subsection is None]
# print('subsection', len(table_4), table_4[:5], '.....')
#
# table_5 = [(x.collection, x.section, x.subsection) for x in catalog.tables.values()
#            if x.chapter == '3' and (None in [x.collection, x.section, x.subsection])]
# print(len(table_5), table_5[:5], '.....')


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



#
# chapters = get_chapters()
# print('Главы:', chapters)
# print('\t', f'Глав: {len(chapters)}')
#
# for chapter_code in chapters:  # [:3]:
#     print(catalog.chapters[chapter_code].title)
#     tables_in_chapter = get_constraints_tables(chapter=chapter_code, collection=None, section=None, subsection=None)
#     if tables_in_chapter:
#         print('\t', 'таблицы: ', len(tables_in_chapter), tables_in_chapter)
#     else:
#         collections = get_chapter_collections(chapter_code)
#         if collections:
#             print('\t', f'сборников: {len(collections)}')
#             for collection_code in collections:
#                 print('\t', extract_int_code(collection_code, 'collection'), catalog.collections[collection_code].title)
#                 tables_in_collections = get_constraints_tables(chapter=chapter_code, collection=collection_code,
#                                                                section=None, subsection=None)
#                 if tables_in_collections:
#                     print('\t' * 2, 'таблицы: ', len(tables_in_collections), tables_in_collections)
#         else:
#             print('\t', 'нет сборников')
#
#
# def available_collections(code):
#     pass
#
#
# def available_sections(code):
#     pass
#
#
# def available_subsections(code):
#     pass
#

def get_selected_tables(**kwargs) -> list[str] | None:
    """chapter_code, collection_code, section_code, subsection_code"""
    kwargs_name = ('chapter', 'collection', 'section', 'subsection')
    nan_char = '*'
    chapter_code, collection_code, section_code, subsection_code = nan_char, nan_char, nan_char, nan_char
    if kwargs:
        chapter_code = kwargs.get('chapter', nan_char)
        collection_code = kwargs.get('collection', nan_char)
        section_code = kwargs.get('section', nan_char)
        subsection_code = kwargs.get('subsection', nan_char)
        vals = [x for x in kwargs.keys() if x in kwargs_name]

        table_codes = []
        if chapter_code != nan_char and collection_code == nan_char and section_code == nan_char and subsection_code == nan_char:
            table_codes = [code for code in catalog.tables.keys() if catalog.tables[code].chapter == chapter_code]
            table_codes.sort(key=lambda code: extract_int_code(code, 'chapter'))
        else:
            if chapter_code != nan_char and collection_code != nan_char and section_code == nan_char and subsection_code == nan_char:
                table_codes = [code for code in catalog.tables.keys()
                               if catalog.tables[code].chapter == chapter_code and
                               catalog.tables[code].collection == collection_code
                               ]
                # fun_key = lambda code: (extract_int_code(code, 'chapter'), extract_int_code(code, 'collection'))
                # table_codes.sort(key=fun_key)
            else:
                if collection_code != nan_char and collection_code != nan_char and section_code != nan_char and subsection_code == nan_char:
                    table_codes = [code for code in catalog.tables.keys()
                                   if catalog.tables[code].chapter == chapter_code and
                                   catalog.tables[code].collection == collection_code and
                                   catalog.tables[code].section == section_code
                                   ]
                else:
                    if collection_code != nan_char and collection_code != nan_char and section_code != nan_char and subsection_code != nan_char:
                        table_codes = [code for code in catalog.tables.keys()
                                       if catalog.tables[code].chapter == chapter_code and
                                       catalog.tables[code].collection == collection_code and
                                       catalog.tables[code].section == section_code and
                                       catalog.tables[code].subsection == subsection_code
                                       ]
        return table_codes if len(table_codes) > 0 else None
    return None


def subsections_out(chapter_code, collection_code, section_code):
    subsections = get_subsection(chapter=chapter_code, collection=collection_code, section=section_code)
    if subsections:
        for subsection in subsections:
            print(f"\t{subsection} {catalog.subsections[subsection].title}")
            print(f"\t\t", get_selected_tables(chapter=chapter_code, collection=collection_code, section=section_code,
                                      subsection=subsection))


def sections_out(chapter_code, collection_code):
    sections = get_section(chapter=chapter_code, collection=collection_code)
    for section in sections:
        print(f"Отдел: {section}")
        print(f"\tтаблицы без разделов: {get_selected_tables(chapter=chapter_code, collection=collection_code, section=section, subsection=None)}")
        subsections_out(chapter_code, collection_code, section)






# def collections_out(chapter_code):
#     for collection in collections:
#         collection_code = ''
#         table_out(chapter_code, collection_code)
#         if available_sections(chapter_code, collection_code):
#             sections_out(chapter_code, collection_code)
#         else:
#             if available_subsections(chapter_code, collection_code):
#                 subsections_out(chapter_code, collection_code)
#
#
# def chapter_out():
#     for chapter_code in chapters:
#         table_out(chapter_code)
#         if available_collections(chapter_code):
#             collections_out(chapter_code)
#         else:
#             if available_sections(chapter_code):
#                 sections_out(chapter_code)
#             else:
#                 if available_subsections(chapter_code):
#                     subsections_out(chapter_code)
#
#
# if chapters:
#     chapter_out()


if __name__ == "__main__":
    application()
    print(f"<< {'-' * 50} >>\n")

    catalog_none_check()
    # ss = [(x.code, x.chapter, x.collection, x.section) for x in catalog.subsections.values() if x.chapter == None or x.collection == None or x.section==None]  # not any((x.section, x.collection, x.chapter))
    # print(f"Разделы с 0-ми главами или сборниками или отделами: {len(ss)} -->", ss)

    # ch = get_chapters()
    # print(f"Главы: {ch}")
    # # chapter = ch[0]
    # for x in ch:
    #     tab = get_selected_tables(chapter=x)
    #     print(f"глава {x}: все {len(tab)} таблицы {tab}") if tab else print(f"глава {x}: Нет таблиц")
    #     tab = get_selected_tables(chapter=x, collection=None)
    #     if tab:
    #         print(f"\t{len(tab)} таблицы для главы {x} у которых нет сборника : {tab}")





    # coll = get_collections(chapter=ch[0])
    # print(f"Сборники для главы {chapter}: {coll}", )
    # tab = get_selected_tables(chapter=chapter, collection=coll[0])
    # print(f"таблицы: {tab}")


    # sections_out(chapter_code='5', collection_code='5.7')


    # subsections_out(chapter_code='5', collection_code='5.7', section_code='5.7-4')

    # code = '19.6-3-51-0-1'
    # code = '19.6-4-88'
    # print(code)
    # print(extract_int_code(code, 'chapter'))
    # print(extract_int_code(code, 'collection'))
    # print(extract_int_code(code, 'section'))
    # print(extract_int_code(code, 'subsection'))
    # t = get_selected_tables(chapter='5', collection='5.7')
    # print(t)
    # t = get_selected_tables(chapter='5', collection='5.7', section='5.7-4')
    # print(t)
    # t = get_selected_tables(chapter='5', collection='5.7', section='5.7-4', subsection='5.7-4-2')
    # print(t)
