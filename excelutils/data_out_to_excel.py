import os

from settings import Catalog, ExcelFile

from excelutils.create_basic_header import create_basic_header
from excelutils.chapters_output import chapters_output
from filesutils import get_full_file_name, does_file_in_use, out_error_message_and_exit


def generate_output_file_name(src_file_name: str) -> str | None:
    """
    Создает новое имя для выходного файла
    :param src_file_name: абсолютное имя файла с данными
    :return:
    """
    path, file = os.path.split(src_file_name)   # имя файла и маршрут
    path = os.path.split(path)[0]               # убираем последнюю папку из маршрута
    output_path = os.path.join(path, "output")  # добавляем в маршрут папку
    output_file = f"renew_{file}"               # изменяем имя файла
    full_name = get_full_file_name(output_file, output_path)
    if full_name and os.path.isfile(full_name):
        if not does_file_in_use(full_name):
            os.remove(full_name)
            return full_name
        else:
            out_error_message_and_exit(f"файл занят другим приложением: ", full_name)
    elif os.path.isdir(output_path):
        return full_name
    else:
        out_error_message_and_exit(f"нет такой папки: ", output_path)
    return None


def data_out_to_excel(catalog: Catalog, data_file: str, grid: bool = False):
    """ Подготовка выходного файла. Создает шапку таблицы. Выводит главы"""
    output_name = generate_output_file_name(data_file)
    output = ExcelFile(output_name)
    with output as ex:
        sheets_name = ["name", "stat"]
        ex.create_sheets(sheets_name)
        ex.styles_init()
        ex.sheet = ex.book['name']
        ex.set_sheet_grid(grid=grid)
        ex.sheet.sheet_properties.outlinePr.summaryBelow = False  # группировка сверху

        create_basic_header(ex.sheet)
        start_chapter_row = 4
        chapters_output(ex.sheet, catalog, start_chapter_row)
        # # вставляем один столбец
        # ex.sheet.insert_cols(1)



