import pandas as pd
import gc
from pandas import DataFrame
import json
from pprint import pprint

from filesutils import check_full_file_name, get_full_file_name, out_error_message_and_exit
from settings import item_patterns, Chapter, Collection, Section, Subsection, Table, Quote, Catalog
from catalog.get_selected_tables import get_selected_tables


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


def chapter_load(data: DataFrame, catalog: Catalog = None):
    """ Загружает 'Главы' в catalog. """
    df = filter_df_data('chapter', data)
    catalog.chapters = {chapter[0]: Chapter(code=chapter[0], title=chapter[1])
                        for chapter in df.to_records(index=False)}
    print(f"Глав добавлено в каталог:: {len(catalog.chapters) = }")
    pprint(list(catalog.chapters.items())[:5], width=200)
    print('....')


def collection_load(data: DataFrame, catalog: Catalog = None):
    """ Загружает 'Сборники' в catalog. """
    df = filter_df_data('collection', data)
    for collection in df.to_records(index=False):
        required_chapter_code = collection[0].split('.')[0]
        chapter_code = get_chapter_code(catalog, required_chapter_code)
        if chapter_code:
            catalog.collections[collection[0]] = Collection(
                code=collection[0], chapter=chapter_code, title=collection[1]
            )
        else:
            out_error_message_and_exit(f"для 'Сборника': {collection}", f"не найдена глава: {required_chapter_code!r}")
    print(f"Сборников добавлено в каталог:: {len(catalog.collections) = }")
    pprint(list(catalog.collections.items())[30:35], width=200)
    print('....')


def section_load(data: DataFrame, catalog: Catalog = None):
    """ Загружает 'Отделы' в catalog. """
    df = filter_df_data('section', data)
    for section in df.to_records(index=False):
        required_chapter_code = section[0].split('.')[0]
        chapter_code = get_chapter_code(catalog, required_chapter_code)
        if chapter_code:
            required_collection_code = section[0].split('-')[0]
            collection_code = get_collection_code(catalog, required_collection_code)
            catalog.sections[section[0]] = Section(
                code=section[0], collection=collection_code, title=section[1], chapter=chapter_code
            )
        else:
            out_error_message_and_exit(f"для 'Отдела': {section}", f"не найдена глава: {required_chapter_code!r}")
    print(f"Отделов добавлено в каталог:: {len(catalog.sections) = }")
    pprint(list(catalog.sections.items())[5:10], width=200)
    null_collection = set([section.code for section in catalog.sections.values() if not section.collection])
    print(f"Отделы с нулевыми 'Сборниками' ({len(null_collection)}): {null_collection=}")
    print('....')


def subsection_load(data: DataFrame, catalog: Catalog = None):
    """ Загружает 'Разделы' в catalog. """
    df = filter_df_data('subsection', data)
    for subsection in df.to_records(index=False):
        required_chapter_code = subsection[0].split('.')[0]
        chapter_code = get_chapter_code(catalog, required_chapter_code)
        if chapter_code:
            required_collection_code = subsection[0].split('-')[0]
            required_section_code = '-'.join(subsection[0].split('-')[:-1])
            collection_code = get_collection_code(catalog, required_collection_code)
            section_code = get_section_code(catalog, required_section_code)
            catalog.subsections[subsection[0]] = Subsection(
                code=subsection[0], title=subsection[1], chapter=chapter_code,
                collection=collection_code, section=section_code,
            )
        else:
            out_error_message_and_exit(f"для 'Раздела': {subsection}", f"не найдена глава: {required_chapter_code!r}")
    print(f"Разделов добавлено в каталог: {len(catalog.subsections) = }")
    pprint(list(catalog.subsections.items())[22:30], width=200)
    null_collection = set([subsection.code for subsection in catalog.subsections.values() if not subsection.collection])
    print(f"Разделы с нулевыми 'Сборниками' ({len(null_collection)}): {null_collection=}")
    null_section = set([
        subsection.code for subsection in catalog.subsections.values() if not subsection.section
    ])
    print(f"Разделы с нулевыми 'Отделами' ({len(null_section)}): {null_section=}")
    print('....')


def table_load(data: DataFrame, catalog: Catalog = None):
    """ Загружает 'Таблицы' в catalog. """
    df = filter_df_data('table', data)
    for table in df.to_records(index=False):
        required_chapter_code = table[0].split('.')[0]
        chapter_code = get_chapter_code(catalog, required_chapter_code)
        if chapter_code:
            required_collection_code = table[0].split('-')[0]
            required_section_code = '-'.join(table[0].split('-')[:2])
            required_subsection_code = '-'.join(table[0].split('-')[:3])

            collection_code = get_collection_code(catalog, required_collection_code)
            section_code = get_section_code(catalog, required_section_code)
            subsection_code = get_subsection_code(catalog, required_subsection_code)

            catalog.tables[table[0]] = Table(
                code=table[0], title=table[1], chapter=chapter_code,
                collection=collection_code, section=section_code, subsection=subsection_code
            )
        else:
            out_error_message_and_exit(f"для 'Таблицы': {table}", f"не найдена глава: {required_chapter_code!r}")
    print(f"Таблиц добавлено в каталог: {len(catalog.tables) = }")
    pprint(list(catalog.tables.items())[20:25], width=200)
    null_collection = set([table.code for table in catalog.tables.values() if not table.collection])
    print(f"Таблицы с нулевыми 'Сборниками' ({len(null_collection)}): {null_collection=}")
    null_section = set([table.code for table in catalog.tables.values() if not table.section])
    print(f"Таблицы с нулевыми 'Отделами' ({len(null_section)}): {null_section=}")
    null_subsection = set([table.code for table in catalog.tables.values() if not table.subsection])
    print(f"Таблицы с нулевыми 'Разделами' ({len(null_subsection)}): {null_subsection=}")
    print('....')


def quotes_load(data: DataFrame, catalog: Catalog = None):
    """ Загружает 'Расценки' в catalog. """
    for quote in data.to_records(index=False):
        catalog.quotes[quote[0]] = Quote(code=quote[0], title=quote[1], measure=quote[2], table=None, chapter=None,
                                         collection=None, section=None, subsection=None)
    print(f"Расценок добавлено в каталог: {len(catalog.quotes) = }")
    pprint(list(catalog.quotes.items())[20:25], width=300)


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
        cut_column_names = df.columns[:2]
        # оставляем только 2 столбца
        df = df.reindex(columns=cut_column_names)
        columns = ['CODE', 'TITLE']
        df.columns = columns
        df = df[columns].astype(pd.StringDtype())
        data_frame_info(df, mode='full')
        #
        chapter_load(df, catalog)
        collection_load(df, catalog)
        section_load(df, catalog)
        subsection_load(df, catalog)
        table_load(df, catalog)
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
        cut_column_names = df.columns[:3]
        # оставляем только 3 столбца
        df = df.reindex(columns=cut_column_names)
        columns = ['CODE', 'TITLE', 'MEASURE']
        df.columns = columns
        df = df[columns].astype(pd.StringDtype())
        data_frame_info(df, mode='full')
        quotes_load(df, catalog)
        del df
        gc.collect()
    else:
        out_error_message_and_exit(f"пустая страница {sheet_name!r}", get_full_file_name(file_name, file_path))
        raise TypeError(OSError)


def quotes_parents_audit(catalog: Catalog = None):
    """ Заполняет поля родителей для всех расценок. Родителей расценки: таблицы, разделы, отделы, сборники, главы. """
    quotes = catalog.quotes
    if len(quotes) > 0:
        print(f"всего расценок в каталоге: ({len(quotes)})")
        for quote in quotes.keys():
            # print(f"расценка {quote=}: {catalog.quotes[quote]}")
            chapter = quote.split('.')[0]
            collection = quote.split('-', 1)[0]
            table_number = quote.split('-')[-2]
            catalog.quotes[quote].chapter = chapter
            catalog.quotes[quote].collection = collection
            # все таблицы для сборника
            tables = get_selected_tables(catalog, selected_chapter=chapter, selected_collection=collection)
            if tables:
                # print(f"все таблицы для сборника: ({len(tables)}): {tables}")
                quote_tables = [x for x in tables if x.split('-')[-1] == table_number]
                # print(f"таблицы для расценки ({len(quote_tables)}): {quote_tables}")
                if quote_tables:
                    # print(f"{catalog.tables[quote_tables[0]].code!r} {catalog.tables[quote_tables[0]].title}")
                    catalog.quotes[quote].table = catalog.tables[quote_tables[0]].code
                    catalog.quotes[quote].subsection = catalog.tables[quote_tables[0]].subsection
                    catalog.quotes[quote].section = catalog.tables[quote_tables[0]].section
                else:
                    catalog.quotes[quote].table = None
                    catalog.quotes[quote].subsection = None
                    catalog.quotes[quote].section = None
            # print(f"расценка: {quotes[quote]}")


def catalog_fill() -> Catalog():
    catalog_item = Catalog()
    path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\Quote_Catalog\src"
    # path = r"C:\Users\kazak.ke\PycharmProjects\Quotes_Catalog\src"
    file = r"catalog_3.xlsx"
    json_name = "catalog.json"
    if check_full_file_name(json_name, path):
        json_full_name = get_full_file_name(json_name, path)
        with open(json_full_name, "r", encoding='utf-8') as j_file:
            catalog_item = Catalog.model_validate_json(json.load(j_file))
    else:
        read_catalog(catalog_item, file, path, sheet_name='catalog')
        read_quotes(catalog_item, file, path, sheet_name='quotes')
        quotes_parents_audit(catalog_item)
        catalog_item.json_damp(json_name, path)

        quotes_without_table = [x for x in catalog_item.quotes.keys() if catalog_item.quotes[x].table is None]
        print(f"расценки без таблиц: {quotes_without_table}")
    return catalog_item



if __name__ == "__main__":
    # catalog = Catalog()
    # catalog.info()
    catalog = catalog_fill()
    catalog.info()

