import os
import sys
from settings import console_colors


def check_full_file_name(file_name: str, file_path: str = "") -> str | None:
    """ Создает абсолютный путь к файлу. Возвращает путь если файл существует """
    if file_name:
        test_path = os.path.abspath(os.path.join(file_path, file_name))
        if os.path.exists(test_path):
            return test_path
    return None


def get_full_file_name(file_name: str, file_path: str) -> str | None:
    """ Создает путь к файлу из файла и маршрута. Проверяет что этот путь корректный """
    if file_name and file_path:
        splicing = os.path.normpath(os.path.join(file_path, file_name))
        if os.path.isabs(splicing):
            return splicing
        output_message(f"Некорректная ссылка:", f" {splicing}")
    return None


def out_error_message_and_exit(error_text: str, file_name: str):
    """ Выводит в консоль сообщение об ошибке при чтении файла.
        Завершает приложение. """
    error_out = f"{console_colors['RED']}{error_text}{console_colors['RESET']}"
    show_full_name = f"'{console_colors['YELLOW']}{file_name}{console_colors['RESET']}'"
    print(f"ошибка обращения к файлу {show_full_name}:\n\t-->> {error_out}")
    sys.exit()


def output_message(text_red: str = None, text_yellow: str = None):
    """ Выводит в консоль сообщение об ошибке. """
    show_red = f"{console_colors['RED']}{text_red}{console_colors['RESET']}"
    show_yellow = f"{console_colors['YELLOW']}{text_yellow}{console_colors['RESET']}"
    print(f"{show_red}:\n\t-->> {show_yellow}")


def location(place_point: str = 'office'):
    match place_point:
        case 'office':
            path_point = r"C:\Users\kazak.ke\PycharmProjects\Quotes_Catalog"
        case 'home':
            path_point = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\Quote_Catalog"
        case _:
            path_point = os.path.abspath(os.getcwd())
            print(f'Неизвестное место {place_point!r}')
    catalog_src_file = r"catalog_3_68.xlsx"
    catalog_json_file_name = f"{catalog_src_file[:-5]}.json"
    parameters_src_file_name = r"template_3_68_output.xlsx"

    src_path = os.path.join(path_point, "src")

    catalog_file = os.path.abspath(os.path.join(src_path, catalog_src_file))
    catalog_json = os.path.abspath(os.path.join(src_path, catalog_json_file_name))
    parameters_src_file = os.path.abspath(os.path.join(src_path, parameters_src_file_name))

    if not os.path.exists(catalog_file):
        out_error_message_and_exit(f"фал с данными для 'Каталога' не найден", f"{catalog_file}")

    if not os.path.exists(parameters_src_file):
        out_error_message_and_exit(f"фал с Параметризацией не найден", f"{parameters_src_file}")

    return catalog_file, catalog_json, parameters_src_file



if __name__ == "__main__":
    fln = "files_tools_setting.py"
    print(f"{os.getcwd() = }")
    print(f"{os.path.dirname(fln) = }")
    print(f"{os.path.exists(fln) = }")

