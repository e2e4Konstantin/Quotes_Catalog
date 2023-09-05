import os


def does_file_in_use(abs_file_name: str) -> bool:
    """ Проверяет, занят или нет указанный по абсолютному маршруту файл
        другим приложением. """
    if abs_file_name and os.path.exists(abs_file_name):
        try:
            os.rename(abs_file_name, abs_file_name)
            return False
        except IOError:
            return True
    return False
