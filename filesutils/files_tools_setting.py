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


def get_full_file_name(file_name: str, file_path: str = "") -> str | None:
    """ Создает абсолютный путь к файлу. """
    if file_name:
        p1 = os.path.join("" if file_path is None else file_path, file_name)
        p2 = os.path.abspath(p1)
        return p2
    return None


def out_error_message_and_exit(error_text: str, file_name: str):
    """ Выводит в консоль сообщение об ошибке при чтении файла.
        Завершает приложение. """
    error_out = f"{console_colors['RED']}{error_text}{console_colors['RESET']}"
    show_full_name = f"'{console_colors['YELLOW']}{file_name}{console_colors['RESET']}'"
    print(f"ошибка обращения к файлу {show_full_name}:\n\t-->> {error_out}")
    sys.exit()


if __name__ == "__main__":
    fln = "files_tools_setting.py"
    print(f"{os.getcwd() = }")
    print(f"{os.path.dirname(fln) = }")
    print(f"{os.path.exists(fln) = }")
    print(f"файл '{fln}' занят: {does_file_in_use(fln)}")
    print(f"файл '' занят: {does_file_in_use('')}")
