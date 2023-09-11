import pandas as pd
import gc
from pandas import DataFrame
import json
from pprint import pprint

from filesutils import check_full_file_name, get_full_file_name, output_message, out_error_message_and_exit
from settings import item_index, classifier, item_patterns, Chapter, Collection, Section, Subsection, Table, Quote, Catalog
from catalog.get_selected_tables import get_selected_tables
from catalog.extract_code import get_numeric_stamp, wildcard_remove, code_type, quote_code_check


def data_frame_info(df: DataFrame, mode: str = 'short'):
    print(df.info(verbose=False, show_counts=True, memory_usage='deep'))
    print(f"использовано памяти: {df.memory_usage(index=True, deep=True).sum():_} bytes")
    print(f"размерность: {df.shape}")
    # print(f"индексы: {df.index}")
    print(f"названия столбцов: {list(df.columns)}")
    print(f"типы данных столбцов: '{df.dtypes.values.tolist()}'")
    print(f"{df.head(5)}") if mode != 'short' else print('<-->')


def filter_df_data(pattern_filter_name: str, data: DataFrame) -> DataFrame:
    code = item_patterns[pattern_filter_name]
    df = data[data['CODE'].str.contains(pat=code, case=False, regex=True)]
    # print(df.head(15))
    # data_frame_info(df)
    print(f"паттерн: {pattern_filter_name!r}: {code!r}, в данных: {len(df.to_records(index=False).tolist())} позиций")
    return df


def get_chapter_code(catalog: Catalog = None, chapter_code: str = "") -> str | None:
    """ Ищет в словаре Главу если находит, то возвращает ее код """
    if chapter_code:
        chapter = catalog.chapters.get(chapter_code, None)
        if chapter:
            return chapter.code
    return None


def get_collection_code(catalog: Catalog = None, collection_code: str = "") -> str | None:
    """ Ищет в словаре Сборник если находит, то возвращает его код """
    if collection_code:
        collection = catalog.collections.get(collection_code, None)
        if collection:
            return collection.code
    return None


def get_section_code(catalog: Catalog = None, section_code: str = "") -> str | None:
    """ Ищет в словаре Отдел если находит, то возвращает его код """
    if section_code:
        section = catalog.sections.get(section_code, None)
        if section:
            return section.code
    return None


def get_subsection_code(catalog: Catalog = None, subsection_code: str = "") -> str | None:
    """ Ищет в словаре Раздел если находит, то возвращает его код """
    if subsection_code:
        subsection = catalog.subsections.get(subsection_code, None)
        if subsection:
            return subsection.code
    return None


def parent_check(parent: str, code: str) -> bool:
    if parent and code and parent == code:
        return True
    # output_message(f"родитель: {parent!r}", f"не совпадает с кодом: {code!r}")
    return False


def chapter_load(data: DataFrame, catalog: Catalog = None, columns: dict[str: int] = None):
    """ Загружает 'Главы' в catalog. """
    df = filter_df_data('chapter', data)
    catalog.chapters = {
        chapter[columns['CODE']]: Chapter(code=chapter[columns['CODE']], title=chapter[columns['TITLE']])
        for chapter in df.to_records(index=False)
    }


def collection_load(data: DataFrame, catalog: Catalog = None, columns_index: dict[str: int] = None):
    """ Загружает 'Сборники' в catalog. """
    df = filter_df_data('collection', data)
    for collection in df.to_records(index=False):
        parent = collection[columns_index['PARENT']]
        code = collection[columns_index['CODE']]
        title = collection[columns_index['TITLE']]
        parts_code = get_numeric_stamp(code, 'collection')
        required_chapter_code = parts_code[0]
        chapter = get_chapter_code(catalog, required_chapter_code)
        if not chapter:
            output_message(f"для 'Сборника': {collection}", f"не найдена глава: {required_chapter_code!r}")
        if not parent_check(parent, chapter):
            output_message(f"для 'Сборника': {collection}", f"не совпадают родитель и код: {parent!r}")
        catalog.collections[code] = Collection(code=code, chapter=chapter, title=title)


def section_load(data: DataFrame, catalog: Catalog = None, columns_index: dict[str: int] = None):
    """ Загружает 'Отделы' в catalog. """
    df = filter_df_data('section', data)
    for section in df.to_records(index=False):
        parent = section[columns_index['PARENT']]
        code = section[columns_index['CODE']]
        title = section[columns_index['TITLE']]

        parts_code = get_numeric_stamp(code, 'section')
        required_chapter_code = parts_code[0]
        required_collection_code = f"{parts_code[0]}.{parts_code[1]}"

        chapter = get_chapter_code(catalog, required_chapter_code)
        collection = get_collection_code(catalog, required_collection_code)

        catalog.sections[code] = Section(code=code, collection=collection, title=title, chapter=chapter)

        if not chapter:
            output_message(f"для 'Отдела': {section}", f"не найдена глава: {required_chapter_code!r}")
        if not collection:
            output_message(f"для 'Отдела': {section}", f"не найден Сборник: {required_collection_code!r}")
        if not (parent_check(parent, chapter) or parent_check(parent, collection)):
            output_message(f"для 'Отдела': {section}", f"не совпадают родитель {parent!r} и код: {code}")


def subsection_load(data: DataFrame, catalog: Catalog = None, columns_index: dict[str: int] = None):
    """ Загружает 'Разделы' в catalog. """
    df = filter_df_data('subsection', data)
    for subsection in df.to_records(index=False):
        parent = subsection[columns_index['PARENT']]
        code = subsection[columns_index['CODE']]
        title = subsection[columns_index['TITLE']]

        parts_code = get_numeric_stamp(code, 'subsection')
        required_chapter_code = parts_code[0]
        required_collection_code = f"{parts_code[0]}.{parts_code[1]}"
        required_section_code = f"{parts_code[0]}.{parts_code[1]}-{parts_code[2]}"

        chapter = get_chapter_code(catalog, required_chapter_code)
        collection = get_collection_code(catalog, required_collection_code)
        section = get_section_code(catalog, required_section_code)

        catalog.subsections[code] = Subsection(
            code=code, title=title, chapter=chapter, collection=collection, section=section
        )

        # if not chapter:
        #     output_message(f"для 'Раздела': {subsection}", f"не найдена глава: {required_chapter_code!r}")
        # if not collection:
        #     output_message(f"для 'Раздела': {subsection}", f"не найден Сборник: {required_collection_code!r}")
        # if not section:
        #     output_message(f"для 'Раздела': {subsection}", f"не найден Отдел: {required_section_code!r}")
        if not (parent_check(parent, chapter) or parent_check(parent, collection) or parent_check(parent, section)):
            output_message(f"для 'Раздела': {subsection}", f"не совпадают родитель {parent!r} и код: {code}")


def table_load(data: DataFrame, catalog: Catalog = None, columns_index: dict[str: int] = None):
    """ Загружает 'Таблицы' в catalog. """
    df = filter_df_data('table', data)
    for table in df.to_records(index=False):
        parent = table[columns_index['PARENT']]
        code = table[columns_index['CODE']]
        title = table[columns_index['TITLE']]

        parts_code = get_numeric_stamp(code, 'table')
        required_chapter_code = parts_code[0]
        required_collection_code = f"{parts_code[0]}.{parts_code[1]}"
        required_section_code = f"{parts_code[0]}.{parts_code[1]}-{parts_code[2]}"
        required_subsection_code = f"{parts_code[0]}.{parts_code[1]}-{parts_code[2]}-{parts_code[3]}"

        chapter = get_chapter_code(catalog, required_chapter_code)
        collection = get_collection_code(catalog, required_collection_code)
        section = get_section_code(catalog, required_section_code)
        subsection = get_subsection_code(catalog, required_subsection_code)

        catalog.tables[code] = Table(
            code=code, title=title, chapter=chapter, collection=collection, section=section, subsection=subsection
        )

        parents = [chapter, collection, section, subsection]
        if True not in set(map(bool, parents)):  # all None
            output_message(f"для Таблицы': {table}", f"нет ни одного родителя {parent!r}")

        # if not chapter:
        #     output_message(f"для Таблицы': {table}", f"не найдена глава: {required_chapter_code!r}")
        # if not collection:
        #     output_message(f"для Таблицы': {table}", f"не найден Сборник: {required_collection_code!r}")
        # if not section:
        #     output_message(f"для Таблицы': {table}", f"не найден Отдел: {required_section_code!r}")
        # if not subsection:
        #     output_message(f"для Таблицы': {table}", f"не найден Раздел: {required_subsection_code!r}")
        # if not (
        #         parent_check(parent, chapter) or parent_check(parent, collection) or
        #         parent_check(parent, section) or parent_check(parent, subsection)
        # ):
        if parent not in parents:
            output_message(f"для Таблицы': {table}", f"не совпадают родитель {parent!r} и код: {code}")


def quotes_load(data: DataFrame, catalog: Catalog = None, columns_index: dict[str: int] = None):
    """ Загружает 'Расценки' в catalog. """
    for quote in data.to_records(index=False):
        parent = quote[columns_index['PARENT']]
        code = quote[columns_index['CODE']]
        title = quote[columns_index['TITLE']]
        measure = quote[columns_index['MEASURE']]

        if not parent or code_type(parent) != item_index['table']:
            output_message(f"для Расценки: {code}", f"кривая родительская таблица: {parent!r}")

        parts_code = get_numeric_stamp(parent, 'table')
        if parts_code:
            table = catalog.tables.get(parent, None)
            table_code = table.code if table else None
            chapter = catalog.chapters.get(parts_code[0], None)
            chapter_code = chapter.code if chapter else None
            collection = catalog.collections.get(f"{parts_code[0]}.{parts_code[1]}", None)
            collection_code = collection.code if collection else None
            section = catalog.sections.get(f"{parts_code[0]}.{parts_code[1]}-{parts_code[2]}", None)
            section_code = section.code if section else None
            subsection = catalog.subsections.get(f"{parts_code[0]}.{parts_code[1]}-{parts_code[2]}-{parts_code[3]}", None)
            subsection_code = subsection.code if subsection else None
            catalog.quotes[code] = Quote(
                code=code, title=title, measure=measure, table=table_code, chapter=chapter_code,
                collection=collection_code, section=section_code, subsection=subsection_code
            )
        else:
            catalog.quotes[code] = Quote(
                code=code, title=title, measure=measure, table=parent,
                chapter=None, collection=None, section=None, subsection=None
            )


def data_frame_turn_out(file_name: str = None, file_path: str = None, sheet_name: str = None,
                        out_file_name: str = "") -> DataFrame | None:
    """ Прочитать данные из файла и вернуть DataFrame """
    if out_file_name:
        parquet_file_name = f"{out_file_name}.gzip"
    else:
        parquet_file_name = f"{file_name[:-4]}gzip"
    parquet_full_name = check_full_file_name(parquet_file_name, file_path)
    df = DataFrame()
    if parquet_full_name:
        try:
            df: DataFrame = pd.read_parquet(parquet_full_name)
        except Exception as err:
            out_error_message_and_exit(str(err), parquet_full_name)
    else:
        full_name = check_full_file_name(file_name, file_path)
        if full_name:
            try:
                df: DataFrame = pd.read_excel(io=full_name, sheet_name=sheet_name)
                columns = df.columns
                df = df[columns].astype(pd.StringDtype())
                pf = get_full_file_name(parquet_file_name, file_path)
                df.to_parquet(pf, compression='gzip')
            except Exception as err:
                out_error_message_and_exit(str(err), full_name)
        else:
            out_error_message_and_exit(f"файл {file_name!r} на найден", f"{file_path}")
    if not df.empty:
        return df
    return None


def read_catalog(catalog: Catalog = None, file_name: str = None, file_path: str = None, sheet_name: str = None):
    """ Читает структуру (таблицы, сборники, отделы, разделы) из excel файла в catalog """
    df = data_frame_turn_out(file_name, file_path, sheet_name, 'p_catalog')
    if (df is not None) and not df.empty:
        cut_column_names = df.columns[:3]
        # оставляем только 3 столбца
        df = df.reindex(columns=cut_column_names)
        columns = ['PARENT', 'CODE', 'TITLE']
        df.columns = columns
        # df = df[columns].astype(pd.StringDtype())
        data_frame_info(df, mode='full')
        #
        columns_index = {column: i for i, column in enumerate(columns)}
        chapter_load(df, catalog, columns_index)
        collection_load(df, catalog, columns_index)
        section_load(df, catalog, columns_index)
        subsection_load(df, catalog, columns_index)
        table_load(df, catalog, columns_index)
        #
        del df
        gc.collect()
    else:
        out_error_message_and_exit(f"пустая страница {sheet_name!r}", get_full_file_name(file_name, file_path))
        raise TypeError(OSError)


def read_quotes(catalog: Catalog = None, file_name: str = None, file_path: str = None, sheet_name: str = None):
    """ Читает расценки из excel файла в catalog """
    df = data_frame_turn_out(file_name, file_path, sheet_name, 'p_quotes')
    if (df is not None) and not df.empty:
        cut_column_names = df.columns[:4]
        # оставляем только 4 столбца
        df = df.reindex(columns=cut_column_names)
        columns = ['PARENT', 'CODE', 'TITLE', 'MEASURE']
        df.columns = columns
        # df = df[columns].astype(pd.StringDtype())
        data_frame_info(df, mode='full')
        columns_index = {column: i for i, column in enumerate(columns)}

        quotes_load(df, catalog, columns_index)
        del df
        gc.collect()
    else:
        out_error_message_and_exit(f"пустая страница {sheet_name!r}", get_full_file_name(file_name, file_path))
        raise TypeError(OSError)


# def quotes_parents_audit(catalog: Catalog = None):
#     """ Заполняет поля родителей для всех расценок. Родителей расценки: таблицы, разделы, отделы, сборники, главы. """
#     quotes = catalog.quotes
#     if len(quotes) > 0:
#         print(f"всего расценок в каталоге: ({len(quotes)})")
#         for quote in quotes.keys():
#             # print(f"расценка {quote=}: {catalog.quotes[quote]}")
#             chapter = quote.split('.')[0]
#             collection = quote.split('-', 1)[0]
#             table_number = quote.split('-')[-2]
#             catalog.quotes[quote].chapter = chapter
#             catalog.quotes[quote].collection = collection
#             # все таблицы для сборника
#             tables = get_selected_tables(catalog, selected_chapter=chapter, selected_collection=collection)
#             if tables:
#                 # print(f"все таблицы для сборника: ({len(tables)}): {tables}")
#                 quote_tables = [x for x in tables if x.split('-')[-1] == table_number]
#                 # print(f"таблицы для расценки ({len(quote_tables)}): {quote_tables}")
#                 if quote_tables:
#                     # print(f"{catalog.tables[quote_tables[0]].code!r} {catalog.tables[quote_tables[0]].title}")
#                     catalog.quotes[quote].table = catalog.tables[quote_tables[0]].code
#                     catalog.quotes[quote].subsection = catalog.tables[quote_tables[0]].subsection
#                     catalog.quotes[quote].section = catalog.tables[quote_tables[0]].section
#                 else:
#                     catalog.quotes[quote].table = None
#                     catalog.quotes[quote].subsection = None
#                     catalog.quotes[quote].section = None
#             # print(f"расценка: {quotes[quote]}")


def catalog_fill() -> Catalog():
    catalog_item = Catalog()
    path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\Quote_Catalog\src"
    # path = r"C:\Users\kazak.ke\PycharmProjects\Quotes_Catalog\src"
    file = r"catalog_4.xlsx"
    json_name = "catalog.json"
    if check_full_file_name(json_name, path):
        json_full_name = get_full_file_name(json_name, path)
        with open(json_full_name, "r", encoding='utf-8') as j_file:
            catalog_item = Catalog.model_validate_json(json.load(j_file))
    else:
        read_catalog(catalog_item, file, path, sheet_name='catalog')
        read_quotes(catalog_item, file, path, sheet_name='quotes')
        catalog_item.json_damp(json_name, path)

        quotes_without_table = [x for x in catalog_item.quotes.keys() if catalog_item.quotes[x].table is None]
        print(f"расценки без таблиц: {quotes_without_table}")
    return catalog_item


if __name__ == "__main__":
    # catalog = Catalog()
    # catalog.info()
    catalog = catalog_fill()
    catalog.details_info()
