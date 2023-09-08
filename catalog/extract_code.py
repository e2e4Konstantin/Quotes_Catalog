import re

from settings import item_index, classifier

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
        '3.1-1-5-0-24' -> (3, 1, 1, 5, 0, 24)"""
    if code:
        extract = re.match(r"^\s*((\d+)\.(\d+)-(\d+)-(\d+)-(\d+)-(\d+))\s*$", code)
        if extract:
            return tuple(map(int, extract.groups()[1:]))
    return None


def get_collection_numeric(code: str = None) -> tuple | None:
    """ Выделяет из шифра сборника и возвращает кортеж целых чисел.
        '3.1' -> (3, 1)"""
    if code:
        extract = re.match(r"^\s*((\d+)\.(\d+))\s*$", code)
        if extract:
            return tuple(map(int, extract.groups()[1:]))
    return None


def get_section_numeric(code: str = None) -> tuple | None:
    """ Выделяет из шифра таблицы числа и возвращает кортеж.
        '3.1-1' -> (3, 1, 1)"""
    if code:
        extract = re.match(r"^\s*((\d+)\.(\d+)-(\d+))\s*$", code)
        if extract:
            return tuple(map(int, extract.groups()[1:]))
    return None

def get_subsection_numeric(code: str = None) -> tuple | None:
    """ Выделяет из шифра таблицы числа и возвращает кортеж.
        '3.1-1-5' -> (3, 1, 1, 5)"""
    if code:
        extract = re.match(r"^\s*((\d+)\.(\d+)-(\d+)-(\d+))\s*$", code)
        if extract:
            return tuple(map(int, extract.groups()[1:]))
    return None


def get_numeric_stamp(code: str = None, target_name: str = '') -> tuple | None:
    """ Выделяет из входного кода значение: главы, сборника, отдела, раздела
        Возвращает кортеж строк. """
    extract = None
    if code:
        match target_name:
            case 'chapter':
                extract = re.match(r"^\s*((\d+))\s*$", code)
            case 'collection':
                extract = re.match(r"^\s*((\d+)\.(\d+))\s*$", code)
            case 'section':
                extract = re.match(r"^\s*((\d+)\.(\d+)-(\d+))\s*$", code)
            case 'subsection':
                extract = re.match(r"^\s*((\d+)\.(\d+)-(\d+)-(\d+))\s*$", code)
            case 'table':
                extract = re.match(r"^\s*((\d+)\.(\d+)-(\d+)-(\d+)-(\d+)-(\d+))\s*$", code)
            case 'quote':
                extract = re.match(r"^\s*((\d+)\.(\d+)-(\d+)-(\d+))\s*", code)
            case _:
                return None
        if extract:
            return tuple(extract.groups()[1:])
    return None


def wildcard_remove(code: str = None)  -> str | None:
    """ Удаляет из строки все символы кроме допустимых """
    return re.sub(r'([.-])\1+', r'\1',
                  re.sub("[^0-9-.]+", r"", code)) if code else None


def code_type(code: str = None) -> int | None:
    """  Определяет что кодирует шифр, кроме шифра расценки, который совпадает с шифром раздела. """
    if code:
        code = wildcard_remove(code)
        match code:
            case check if check.isdigit():
                return item_index['chapter']
            case check if re.fullmatch(r"^\s*((\d+)\.(\d+))\s*$", check):
                return item_index['collection']
            case check if re.fullmatch(r"^\s*((\d+)\.(\d+)-(\d+))\s*$", check):
                return item_index['section']
            case check if re.fullmatch(r"^\s*((\d+)\.(\d+)-(\d+)-(\d+))\s*$", check):
                return item_index['subsection']
            case check if re.fullmatch(r"^\s*((\d+)\.(\d+)-(\d+)-(\d+)-(\d+)-(\d+))\s*$", check):
                return item_index['table']
            case _:
                return None
    return None


def quote_code_check(code: str = None) -> int | None:
    """  Определяет что шифр кодирует расценку. """
    if code and re.fullmatch(r"^\s*((\d+)\.(\d+)-(\d+)-(\d+))\s*", wildcard_remove(code)):
        return item_index['quote']
    return None


if __name__ == "__main__":
    print(wildcard_remove('7.\96----4^%&^....(*&)(*&\t\n'))

    print(classifier[code_type('7')])
    print(classifier[code_type('9.51')])
    print(classifier[code_type('9.3-7')])
    print(classifier[code_type('9.3-7-77')])
    print(classifier[code_type('9.3-7-2-4-33')])
    print(classifier[code_type('  #$%\t3#$%\t.3-7-2#$%\t')])
    x = code_type('3.3-7-2-9-9-6')
    print(classifier[x]) if x else print(x)
    print(classifier[quote_code_check('9.3-7-77')])


    # print(get_section_numeric('7.9-2'))
    # print(get_subsection_numeric('7.9-2-61'))
    # print(get_table_numeric('7.9-2-88-24-71'))
    # print()
    print(get_numeric_stamp('7', 'chapter'))
    print(get_numeric_stamp('3.0', 'collection'))
    print(get_numeric_stamp('7.9-5', 'section'))
    print(get_numeric_stamp('7.9-5-88', 'subsection'))
    print(get_numeric_stamp('3.1-1-5-0-2', 'table'))
    print(get_numeric_stamp('3.11-59-2', 'quote'))
