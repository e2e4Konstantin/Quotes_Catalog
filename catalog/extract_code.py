import re


def extract_int_code(code: str = None, target_name: str = '') -> int | None:
    """ Выделяет из входного кода целочисленное значение: главы, сборника, отдела, раздела """
    extract = None
    if code:
        match target_name:
            case 'chapter':
                extract = re.match(r"^\s*(\d+)", code)
                extract = extract.group(1).split('.', 1)[0] if extract else None
            case 'collection':
                extract = re.match(r"^\s*(\d+\.\d+)", code)
                extract = extract.group(1).split('.')[1].split('-', 1)[0] if extract else None
            case 'section':
                extract = re.match(r"^\s*(\d+\.\d+-\d+)", code)
                extract = extract.group(1).split('-', 2)[1] if extract else None
            case 'subsection':
                extract = re.match(r"^\s*(\d+\.\d+(-\d+){2})", code)
                extract = extract.group(1).split('-', 3)[2] if extract else None
            case _:
                return None
    return int(extract) if extract and isinstance(extract, str) and extract.isdigit() else None


def get_quote_numeric(code: str = None) -> tuple | None:
    """ Выделяет из шифра расценки числа и возвращает кортеж.
        '4.1-2-10' -> (4, 1, 2, 10)"""
    if code:
        extract = re.match(r"^\s*((\d+)\.(\d+)-(\d+)-(\d+))\s*", code)
        if extract:
            return tuple(map(int, extract.groups()[1:]))
    return None


def get_table_numeric(code: str = None) -> tuple | None:
    """ Выделяет из шифра таблицы числа и возвращает кортеж.
        '3.1-1-5-0-24' -> ('3', '1', '1', '5', '0', '24')"""
    if code:
        extract = re.match(r"^\s*((\d+)\.(\d+)-(\d+)-(\d+)-(\d+)-(\d+))\s*$", code)
        if extract:
            return tuple(map(int, extract.groups()[1:]))
    return None


def get_collection_numeric(code: str = None) -> tuple | None:
    """ Выделяет из шифра сборника и возвращает кортеж целых чисел.
        '3.1' -> ('3', '1')"""
    if code:
        extract = re.match(r"^\s*((\d+)\.(\d+))\s*$", code)
        if extract:
            return tuple(map(int, extract.groups()[1:]))
    return None
