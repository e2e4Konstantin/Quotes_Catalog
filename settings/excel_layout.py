# https://htmlcolorcodes.com/
# https://htmlcolorcodes.com/color-chart/

from openpyxl.styles import Color

headers = {
    'A:O': ['глава', 'сборник', 'отдел', 'раздел', 'таблица', 'расценка',
            'Наименование главы, сборника, отдела, раздела, таблицы, расценки', 'Измеритель',
            'стат.', 'флаг.пар', 'основная',
            'родитель', 'алгоритм', 'элемент', 'материал'],

    'P:T': ['от', 'до', 'ед.изм.', 'шаг', 'тип'],

    'K1': 'Дополнительные расценки',
    'N1': 'Атрибуты',
    'P1': 'Название_параметра',

    'K': 'основная',
    'L': 'родитель',
    'M': 'алгоритм',
    'N': 'элемент',
    'O': 'материал',
}

width_columns = {'A': 6, 'B': 6, 'C': 6, 'D': 6, 'E': 8, 'F': 7, 'G': 45, 'H': 7, 'I': 7, 'J': 7, 'K': 7, 'L': 7, 'M': 7}


colors_styling = {'further_quotes': 'F9FAFA', 'table_name': 'EEF3F8', 'attributes': 'F1F1F9', 'parameters': 'EFF6F2', 'title_basic': "00FAFAF4", 'title_attributes': "00daeef3", 'title_parameter': "00fde9d9", 'c3': "0099CC00", 'c4': "00FFCC00", 'c5': "000066CC", 'c6': "00666699", 'c7': "00C0C0C0", 'c8': "00FF99CC"}

cell_styles = [
    {
        'name':       'title_basic',
        'font':       {'name': 'Calibri', 'bold': False, 'size': 8},
        'alignment':  {'horizontal': 'center', 'vertical': 'bottom', 'wrap_text': True, 'shrink_to_fit': False, 'indent': 0},
        'fill':       {'patternType': "solid", 'fgColor': colors_styling['title_basic']},
        'border':     {'style': 'thin', 'color': "A0A0A0"}
    },
    #
    {
        'name':       'further_quotes',
        'font':       {'name': 'Calibri', 'bold': False, 'size': 8},
        'alignment':  {'horizontal': 'left', 'vertical': 'bottom', 'wrap_text': True, 'shrink_to_fit': False, 'indent': 0},
        'fill':       {'patternType': "solid", 'fgColor': colors_styling['further_quotes']},
        'border':     {'style': 'thin', 'color': "A0A0A0"}
    },
    {
        'name':       'title_parameter',
        'font':       {'name': 'Calibri', 'bold': False, 'size': 8},
        'alignment':  {'horizontal': 'left', 'vertical': 'bottom', 'wrap_text': True, 'shrink_to_fit': False, 'indent': 0},
        'fill':       {'patternType': "solid", 'fgColor': colors_styling['parameters']},
        'border':     {'style': 'thin', 'color': "A0A0A0"}
    },
    {
        'name':       'title_attributes',
        'font':       {'name': 'Calibri', 'bold': False, 'size': 8},
        'alignment':  {'horizontal': 'left', 'vertical': 'bottom', 'wrap_text': False, 'shrink_to_fit': False, 'indent': 0},
        'fill':       {'patternType': "solid", 'fgColor': colors_styling['attributes']},
        'border':     {'style': 'thin', 'color': "A0A0A0"}
    },
    {
        'name':       'code_quotes',
        'font':       {'name': 'Calibri', 'bold': True, 'size': 8},
        'alignment':  {'horizontal': 'left', 'vertical': 'bottom', 'wrap_text': False, 'shrink_to_fit': False, 'indent': 0},
        'fill':       {'patternType': None, 'fgColor': colors_styling['title_attributes']},
        'border':     {'style': None, 'color': "000000"}
    },
    {
        'name':       'line_table',
        'font':       {'name': 'Calibri', 'bold': False, 'size': 8},
        'alignment':  {'horizontal': 'left', 'vertical': 'bottom', 'wrap_text': False, 'shrink_to_fit': False, 'indent': 0},
        'fill':       {'patternType': None, 'fgColor': colors_styling['title_attributes']},
        'border':     {'style': None, 'color': "000000"}
    },
{
        'name':       'table_name',
        'font':       {'name': 'Calibri', 'bold': False, 'size': 8, 'color': "000000"},
        'alignment':  {'horizontal': 'left', 'vertical': 'bottom', 'wrap_text': False, 'shrink_to_fit': False, 'indent': 0},
        'fill':       {'patternType': "solid", 'fgColor': colors_styling['table_name']},
        'border':     {'style': None, 'color': "000000"}
    },

    {
        'name':       'quote_line',
        'font':       {'name': 'Calibri', 'bold': False, 'size': 8, 'color': "000000"},
        'alignment':  {'horizontal': 'left', 'vertical': 'bottom', 'wrap_text': False, 'shrink_to_fit': False, 'indent': 0},
        'fill':       {'patternType': None, 'fgColor': colors_styling['title_attributes']},
        'border':     {'style': None, 'color': "000000"}
    },

    {
        'name':       'chapter_line',
        'font':       {'name': 'Calibri', 'bold': False, 'size': 8, 'color': Color(rgb='00FF0000')},
        'alignment':  {'horizontal': 'left', 'vertical': 'bottom', 'wrap_text': False, 'shrink_to_fit': False, 'indent': 0},
        'fill':       {'patternType': None, 'fgColor': "FFFFFF"},
        'border':     {'style': None, 'color': "000000"}
    }

]
