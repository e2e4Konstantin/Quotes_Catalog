# a = [('Al', 2),('Bill', 1),('Carol', 2), ('Abel', 3), ('Zeke', 2), ('Chris', 1), ('Bill', 3), ('Bill', 5)]
#
# s = sorted(a, key=lambda x: (x[0], x[1]))
# print(s)



import re
import random


def get_quote_numeric(code: str = None) -> tuple | None:
    if code:
        extract = re.match(r"^\s*((\d+)\.(\d+)-(\d+)-(\d+))\s*", code)
        if extract:
            # print(extract.groups()[1:])
            return tuple(map(int, extract.groups()[1:]))
    return None



d = ['3.1-1-6', '4.1-2-10', '4.1-5-7',  '4.1-3-2', '3.3-2-11', '1.1-2-12', '1.1-3-1', '4.7-3-2', '3.7-4-1']
random.shuffle(d)
print(d)

for x in d:
    print(get_quote_numeric(x))

s = sorted(d, key=lambda x: get_quote_numeric(x))
print(s)

def get_table_numeric(code: str = None) -> tuple | None:
    """ Выделяет из шифра таблицы числа и возвращает кортеж.
        '3.1-1-5-0-24' -> ('3', '1', '1', '5', '0', '24')"""
    if code:
        extract = re.match(r"^\s*((\d+)\.(\d+)-(\d+)-(\d+)-(\d+)-(\d+))\s*$", code)
        if extract:
            return tuple(map(int, extract.groups()[1:]))
    return None

print(get_table_numeric('3.1-1-5-0-24'))


def get_collection_numeric(code: str = None) -> tuple | None:
        # 3.15 -> ('3', '15')

    if code:
        extract = re.match(r"^\s*((\d+)\.(\d+))\s*$", code)
        if extract:
            return tuple(map(int, extract.groups()[1:]))
    return None


coll = ['3.27', '3.28', '3.29', '3.30']
for x in coll:
    print(get_collection_numeric(x))


