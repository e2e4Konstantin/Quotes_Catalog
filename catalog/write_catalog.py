from settings import catalog
from read_catalog import read_catalog
import random


def application():
    # path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\Quote_Catalog\src"
    path = r"C:\Users\kazak.ke\PycharmProjects\Quotes_Catalog\src"
    file = r"catalog_3.xlsx"
    sheet = 'catalog'
    read_catalog(file, path, sheet)


application()


table_0 = [catalog.tables[i].code for i in catalog.tables.keys()]
print(len(table_0))
table_1 = [catalog.tables[i].code for i in catalog.tables.keys() if catalog.tables[i].chapter == '3']
print(len(table_1))
table_2 = [x.code for x in catalog.tables.values() if x.chapter == '3' and x.collection is None]
print('collection', len(table_2), table_2[:5], '.....')

table_3 = [x.code for x in catalog.tables.values() if x.chapter == '3' and x.section is None]
print('section', len(table_3), table_3[:5], '.....')

table_4 = [x.code for x in catalog.tables.values() if x.chapter == '3' and x.subsection is None]
print('subsection', len(table_4), table_4[:5], '.....')

table_5 = [(x.collection, x.section, x.subsection) for x in catalog.tables.values()
           if x.chapter == '3' and (None in [x.collection, x.section, x.subsection])]
print(len(table_5), table_5[:5], '.....')



chapters_rank = list(catalog.chapters.keys())
chapters_rank.sort(key=lambda x: int(x.strip()))
# print(type(chapters_rank), chapters_rank)

for chapter in chapters_rank:
    print(catalog.chapters[chapter].title)
    # таблицы без сборников
    table_non_collections = [x.code for x in catalog.tables.values() if x.chapter == chapter and x.collection is None]
    if len(table_non_collections) > 0:
        print(table_non_collections)
    else:
        collections_rank = [x for x in catalog.collections.keys() if catalog.collections[x].chapter == chapter]
        collections_rank.sort(key=lambda x: int(x.split('.')[1]))
        # print(collections_rank)
        for collection in collections_rank:
            print(f"\t{catalog.collections[collection].title}")
            table_non_section = [x.code for x in catalog.tables.values() if x.chapter == chapter and x.collection == collection and x.section is None]
            if len(table_non_section) > 0:
                print('\t\tтаблицы: ', table_non_section)
            else:
                section_rank = [x for x in catalog.sections.keys()
                                if catalog.sections[x].chapter == chapter and catalog.sections[x].collection == collection]
                section_rank.sort(key=lambda x: int(x.split('-')[1]))
                # print('\t\t отделы ', section_rank)
                for section in section_rank:
                    print(f"\t\t{catalog.sections[section].title}")
                    table_non_subsection = [x.code for x in catalog.tables.values()
                                            if x.chapter == chapter
                                            and x.collection == collection
                                            and x.section == section
                                            and x.subsection is None]
                    if len(table_non_subsection) > 0:
                        print('\t\t\tтаблицы: ', table_non_subsection)