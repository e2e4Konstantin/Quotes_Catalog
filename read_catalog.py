import pandas as pd
from pandas import DataFrame
from filesutils import check_full_file_name, get_full_file_name, out_error_message_and_exit
from settings import item_patterns, catalog, Chapter, Collection, Section, Subsection

import gc


def data_frame_info(df: DataFrame, mode: str = 'short'):
    print(df.info(verbose=False, show_counts=True, memory_usage='deep'))
    print(f"использовано памяти: {df.memory_usage(index=True, deep=True).sum():_} bytes")
    print(f"размерность: {df.shape}")
    # print(f"индексы: {df.index}")
    print(f"названия столбцов: {list(df.columns)}")
    print(f"типы данных столбцов: '{df.dtypes.values.tolist()}'")
    print(f"{df.head(5)}") if mode != 'short' else print('<-->')


def get_items_from_data_frame(data: DataFrame):
    code = item_patterns['chapter']
    df = data[data['CODE'].str.contains(pat=code, case=False, regex=True)]
    # print(df.head(15))
    # data_frame_info(df)
    print(f"паттерн: {code}, в списке: {len(df.to_records(index=False).tolist())} позиций")
    catalog.chapters = [Chapter(code=chapter[0], title=chapter[1]) for chapter in df.to_records(index=False).tolist()]
    print(f"добавлено: {len(catalog.chapters)=} {catalog.chapters=}")

    code = item_patterns['collection']
    df = data[data['CODE'].str.contains(pat=code, case=False, regex=True)]
    # print(df.head(15))
    # data_frame_info(df)
    print(f"паттерн: {code}, в списке: {len(df.to_records(index=False).tolist())} позиций")
    for collection in df.to_records(index=False).tolist():
        parent_chapter = '0'
        for chapter in catalog.chapters:
            if collection[0].split('.')[0] == chapter.code:
                parent_chapter = chapter.code
                # print(f"\tглава найдена: {chapter}")
                break
        catalog.collections.append(Collection(code=collection[0], chapter=parent_chapter, title=collection[1]))
    all_chapters = set([collection.chapter for collection in catalog.collections])
    print(f"добавлено: {len(catalog.collections)=}\n{catalog.collections=}\n{all_chapters=}")

    code = item_patterns['section']
    df = data[data['CODE'].str.contains(pat=code, case=False, regex=True)]
    # print(df.head(15))
    # data_frame_info(df)
    print(f"паттерн: {code}, в списке: {len(df.to_records(index=False).tolist())} позиций")

    for section in df.to_records(index=False).tolist():
        parent_collection = '0.0'
        for collection in catalog.collections:
            if section[0].split('-')[0] == collection.code:
                parent_collection = collection.code
                # print(f"\tсборник найден: {collection}")
                break
        catalog.sections.append(Section(code=section[0], collection=parent_collection, title=section[1]))
    all_collections = set([section.collection for section in catalog.sections])
    print(f"добавлено: {len(catalog.sections)=}\n{catalog.sections=}\n{all_collections=}")
    if '0.0' in all_collections:
        print(f"есть нулевые сборники")


    code = item_patterns['subsection']
    df = data[data['CODE'].str.contains(pat=code, case=False, regex=True)]
    print(df.head(15))
    data_frame_info(df)
    print(f"паттерн: {code}, в списке: {len(df.to_records(index=False).tolist())} позиций")

    for subsection in df.to_records(index=False).tolist():
        print(subsection)
        parent_section = '0.0-0'
        for section in catalog.sections:
            search_code = '-'.join(subsection[0].split('-')[:-1])
            # print(search_code, section)
            if search_code == section.code:
                parent_section = section.code
                # print(f"\tотдел найден: {section}")
                break
        catalog.subsections.append(Subsection(code=subsection[0], section=parent_section, title=subsection[1]))
    null_sections = set([(subsection.code, subsection.section) for subsection in catalog.subsections if subsection.section == '0.0-0'])
    print(f"добавлено: {len(catalog.subsections)=}\n{catalog.subsections=}\n{null_sections=}")
    if '0.0-0' in null_sections:
        print(f"в Разделах есть нулевые Отделы")
        parent_collection = '0.0'
        for collection in catalog.collections:
            search_code = subsection[0].split('-')[0]
            if search_code == collection.code:
                parent_collection = collection.code
                # print(f"\tсборник найден: {collection}")
                break




def data_frame_turn_out(file_name: str = None, file_path: str = None, sheet_name: str = None) -> DataFrame | None:
    """ Прочитать данные из файла и вернуть DataFrame """
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
    if not df.empty:
        return df
    return None


def read_catalog(file_name: str = None, file_path: str = None, sheet_name: str = None):
    df = data_frame_turn_out(file_name, file_path, sheet_name)
    if (df is not None) and not df.empty:
        df.columns = ['CODE', 'TITLE']
        df = df[['CODE', 'TITLE']].astype(pd.StringDtype())
        data_frame_info(df, mode='full')
        get_items_from_data_frame(df)
        del df
        gc.collect()
    else:
        out_error_message_and_exit(f"пустая страница {sheet_name!r}", get_full_file_name(file_name, file_path))
        raise TypeError(OSError)


if __name__ == "__main__":
    path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\Quote_Catalog\src"
    file = r"catalog_3.xlsx"
    sheet = 'catalog'
    read_catalog(file, path, sheet)
