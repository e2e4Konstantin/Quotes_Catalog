from pydantic import BaseModel, Field

classifier = ['chapters', 'collections', 'sections', 'subsections', 'tables']

item_patterns = {
    'quote': r"^\s*\d+\.\d+(-\d+){2}\s*$",  # 3.1-24-1 Расценка
    'table': r"^\s*\d+\.\d+(-\d+){4}\s*$",  # 3.1-1-5-0-24 Таблица
    'subsection': r"^\s*\d+\.\d+-\d+-\d+\s*$",  # 3.1-1-5 Раздел
    'section': r"^\s*\d+\.\d+-\d+\s*$",  # 7.9-1 Отдел
    'collection': r"^\s*\d+\.\d+\s*$",  # 7.9 Сборник
    'chapter': r"^\s*\d+\s*$",  # 7 Глава
}


class Quote(BaseModel):
    code: str = Field(pattern=item_patterns['quote'])  # 3.1-24-1
    title: str
    table: str = Field(pattern=item_patterns['table'])  # 3.1-1-5-0-24
    subsection: str | None = None
    section: str | None = None
    collection: str | None = None
    chapter: str | None = None


class Table(BaseModel):
    code: str = Field(pattern=item_patterns['table'])  # 9.1-1-1-0-2
    title: str
    subsection: str | None = Field(pattern=item_patterns['subsection'])  # 3.1-1-5
    section: str | None = None
    collection: str | None = None
    chapter: str | None = None


# 8.2-1-1 Раздел 1.1.1. Ультразвуковой контроль и механические испытания сварных соединений газопроводов
class Subsection(BaseModel):
    code: str = Field(pattern=item_patterns['subsection'])
    title: str
    section: str = Field(pattern=item_patterns['section'])
    collection: str | None = None
    chapter: str | None = None


# 8.2-1	Отдел 1.1. Контроль качества сварных соединений
class Section(BaseModel):
    code: str = Field(pattern=item_patterns['section'])
    title: str
    collection: str = Field(pattern=item_patterns['collection'])
    chapter: str | None = None


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
    quotes: list[Quote] | None = []
    tables: list[Table] | None = []
    subsections: list[Subsection] | None = []
    sections: list[Section] | None = []
    collections: list[Collection] | None = []
    chapters: list[Chapter] | None = []

catalog = Catalog()



if __name__ == "__main__":
    info_quote = {'code': '3.1-24-1',
                  'title': 'Срезка недобора грунта в выемках группа грунтов 1-3',
                  'table': '3.1-1-5-0-24'}
    quote = Quote(**info_quote)
    table = Table(code='9.1-1-1-0-2', subsection='9.1-1-1',
                  title='Временное отопление, законченных вчерне производственных зданий промышленных предприятий')
    subsection = Subsection(code='8.2-1-1', section='8.2-1',
                            title='Ультразвуковой контроль и механические испытания сварных соединений газопроводов')
    section = Section(code='8.2-1', collection='8.2', title='Контроль качества сварных соединений')
    collection = Collection(code='8.2', chapter='8',
                            title='Контроль качества соединений стальных и полиэтиленовых газопроводов')
    chapter = Chapter(code='8', title='Нормы накладных расходов и сметной прибыли')

    print(f" {quote=}\n {table=}\n {subsection=}\n {section=}\n {collection=}\n {chapter=}")
    print(f"{catalog=}")




