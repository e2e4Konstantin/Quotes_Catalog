import re
from pprint import pprint

from pydantic import BaseModel, Field
import json

import os

classifier = ['chapter', 'collection', 'section', 'subsection', 'table', 'quote']

item_index = {item: i for i, item in enumerate(classifier)}

legal_chars_pattern = re.compile("[^0-9-.]+")

item_patterns = {
    'quote': r"^\s*\d+\.\d+(-\d+){2}\s*$",  # 3.1-24-1 Расценка
    'table': r"^\s*\d+\.\d+-\d+-\d+-\d+-\d+\s*$",  # 3.1-1-5-0-24 Таблица
    'subsection': r"^\s*\d+\.\d+-\d+-\d+\s*$",  # 3.1-1-5 Раздел
    'section': r"^\s*\d+\.\d+-\d+\s*$",  # 7.9-1 Отдел
    'collection': r"^\s*\d+\.\d+\s*$",  # 7.9 Сборник
    'chapter': r"^\s*\d+\s*$",  # 7 Глава
}


class Quote(BaseModel):
    code: str = Field(pattern=item_patterns['quote'])  # 3.1-24-1
    title: str
    measure: str
    stat: int | None = None
    flag: str = ""
    basic_slave: str = ""
    link_cod: str = ""
    table: str | None = Field(pattern=item_patterns['table'])  # 3.1-1-5-0-24
    subsection: str | None = Field(pattern=item_patterns['subsection'])
    section: str | None = Field(pattern=item_patterns['section'])
    collection: str | None = Field(pattern=item_patterns['collection'])
    chapter: str | None = Field(pattern=item_patterns['chapter'])


class Table(BaseModel):
    code: str = Field(pattern=item_patterns['table'])  # 9.1-1-1-0-2
    title: str
    subsection: str | None = Field(pattern=item_patterns['subsection'])  # 3.1-1-5
    section: str | None = Field(pattern=item_patterns['section'])
    collection: str | None = Field(pattern=item_patterns['collection'])
    chapter: str = Field(pattern=item_patterns['chapter'])
    attributes: str = ""
    parameters: str = ""


# 8.2-1-1 Раздел 1.1.1. Ультразвуковой контроль и механические испытания сварных соединений газопроводов
class Subsection(BaseModel):
    code: str = Field(pattern=item_patterns['subsection'])
    title: str
    section: str | None = Field(pattern=item_patterns['section'])
    collection: str | None = Field(pattern=item_patterns['collection'])
    chapter: str = Field(pattern=item_patterns['chapter'])


# 8.2-1	Отдел 1.1. Контроль качества сварных соединений
class Section(BaseModel):
    code: str = Field(pattern=item_patterns['section'])
    title: str
    collection: str | None = Field(pattern=item_patterns['collection'])
    chapter: str = Field(pattern=item_patterns['chapter'])


# 8.2 Сборник 2. Контроль качества соединений стальных и полиэтиленовых газопроводов
class Collection(BaseModel):
    code: str = Field(pattern=item_patterns['collection'])
    title: str
    chapter: str = Field(pattern=item_patterns['chapter'])


# 8	Глава 8. Нормы накладных расходов и сметной прибыли
class Chapter(BaseModel):
    code: str = Field(pattern=item_patterns['chapter'])
    title: str


class Catalog(BaseModel):
    quotes: dict[str, Quote] | None = {}
    tables: dict[str, Table] | None = {}
    subsections: dict[str, Subsection] | None = {}
    sections: dict[str, Section] | None = {}
    collections: dict[str, Collection] | None = {}
    chapters: dict[str, Chapter] | None = {}

    def json_damp(self, file_name: str = "", path: str = ""):
        if file_name:
            full_name = os.path.abspath(os.path.join("" if path is None else path, file_name))
        else:
            full_name = r"catalog.json"
        with open(full_name, "w", encoding='utf-8') as j_file:
            json.dump(self.model_dump_json(), j_file, ensure_ascii=False)

    def info(self):
        print(f"В каталоге:")
        print("\t", f"глав: {len(self.chapters)}")
        print("\t", f"сборников: {len(self.collections)}")
        print("\t", f"отелов: {len(self.sections)}")
        print("\t", f"разделов: {len(self.subsections)}")
        print("\t", f"расценок: {len(self.quotes)}")

    def details_info(self):
        print(f"В каталоге:")
        print(f"Глав: {len(self.chapters) = }")
        print(f"Сборников: {len(self.collections) = }")
        print(f"Отделов: {len(self.sections) = }")
        print(f"Разделов: {len(self.subsections) = }")
        print(f"Таблиц: {len(self.tables) = }")
        print(f"Расценок: {len(self.quotes) = }")

        print('....')
        pprint(list(self.chapters.items())[:3], width=200)
        print('....')
        pprint(list(self.collections.items())[5:8], width=200)
        null_chapter = set([collection.code for collection in self.collections.values() if not collection.chapter])
        print(f"Сборники с нулевыми 'Главами' ({len(null_chapter)}): {null_chapter=}")
        print('....')
        pprint(list(self.sections.items())[5:8], width=200)
        null_chapter = set([section.code for section in self.sections.values() if not section.chapter])
        null_collection = set([section.code for section in self.sections.values() if not section.collection])
        print(f"Отделы с нулевыми 'Главами' ({len(null_chapter)}): {null_chapter=}")
        print(f"Отделы с нулевыми 'Сборниками' ({len(null_collection)}): {null_collection=}")
        print('....')
        pprint(list(self.subsections.items())[5:8], width=200)
        null_chapters = set([subsection.code for subsection in self.subsections.values() if not subsection.chapter])
        null_collection = set(
            [subsection.code for subsection in self.subsections.values() if not subsection.collection]
        )
        null_section = set(
            [subsection.code for subsection in self.subsections.values() if not subsection.section]
        )
        print(f"Разделы с нулевыми 'Главами' ({len(null_chapters)}): {null_chapters=}")
        print(f"Разделы с нулевыми 'Сборниками' ({len(null_collection)}): {null_collection=}")
        print(f"Разделы с нулевыми 'Отделами' ({len(null_section)}): {null_section=}")
        print('....')

        pprint(list(self.tables.items())[5:8], width=300)
        null_chapters = set([table.code for table in self.tables.values() if not table.chapter])
        null_collection = set([table.code for table in self.tables.values() if not table.collection])
        null_section = set([table.code for table in self.tables.values() if not table.section])
        null_subsection = set([table.code for table in self.tables.values() if not table.subsection])
        print(f"Таблицы с нулевыми 'Главами' ({len(null_chapters)}): {null_chapters=}")
        print(f"Таблицы с нулевыми 'Сборниками' ({len(null_collection)}): {null_collection=}")
        print(f"Таблицы с нулевыми 'Отделами' ({len(null_section)}): {null_section=}")
        print(f"Таблицы с нулевыми 'Разделами' ({len(null_subsection)}): {null_subsection=}")
        print('....')
        pprint(list(self.quotes.items())[5:8], width=300)
        null_tables = set([quote.code for quote in self.quotes.values() if not quote.table])
        print(f"Расценки с нулевыми 'Таблицами' ({len(null_tables)}): {null_tables=}")
        print('....')












if __name__ == "__main__":
    quote = Quote(code='3.1-24-1', title='Срезка недобора грунта в выемках группа грунтов 1-3',
                  measure='100 м3 грунта', table='3.1-1-5-0-24', chapter='9', collection=None, section=None, subsection=None)
    print(quote)
    # table = Table(code='9.1-1-1-0-2', subsection='9.1-1-1',
    #               title='Временное отопление, законченных вчерне производственных зданий промышленных предприятий',
    #               chapter='9', collection=None, section=None)
    # subsection = Subsection(code='8.2-1-1', section='8.2-1', chapter='8', collection=None,
    #                         title='Ультразвуковой контроль и механические испытания сварных соединений газопроводов')
    # section = Section(code='8.2-1', collection='8.2', title='Контроль качества сварных соединений', chapter='8')
    # collection = Collection(code='8.2', chapter='8',
    #                         title='Контроль качества соединений стальных и полиэтиленовых газопроводов')
    # chapter = Chapter(code='8', title='Нормы накладных расходов и сметной прибыли')

    catalog = Catalog()
    #
    # print(f" {quote=}\n {table=}\n {subsection=}\n {section=}\n {collection=}\n {chapter=}")
    # print(f"{catalog=}, {catalog.model_dump()}")
    catalog.quotes[quote.code] = quote
    print(f"{catalog.quotes[quote.code]}")
    # catalog.tables[table.code] = table
    print(f"{catalog=}, {catalog.model_dump()}")
