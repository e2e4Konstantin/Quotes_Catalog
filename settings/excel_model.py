import sys
import openpyxl
from filesutils import does_file_in_use
from settings import console_colors


class ExcelFile:
    def __init__(self, full_file_name: str = None):
        self.file_name = full_file_name
        self.sheet_name = None
        self.book = None
        self.sheet = None

    def __enter__(self):
        """ Вызывается при старте контекстного менеджера. Открывает книгу, создает листы. """
        self.open_excel_file()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """ Будет вызван в завершении конструкции with, или в случае возникновения ошибки после нее. """
        self.close_excel_file()

    def __str__(self):
        return f"excel file: '{self.file_name}', sheet: '{self.sheet_name}', *: '{self.sheet}'"

    def open_excel_file(self):
        """ Создает новый excel файл. """
        try:
            self.book = openpyxl.Workbook()     # создаем новый файл
        except IOError as err:
            error_out = f"{console_colors['RED']}{err}{console_colors['RESET']}"
            print(f"Ошибка при создании файла: '{self.file_name}'\n\t{error_out}")
            sys.exit()

    def close_excel_file(self):
        if does_file_in_use(self.file_name):
            print(f"Не могу записать файл {self.file_name}, он используется другим приложением.")
        else:
            if self.book:
                self.book.save(self.file_name)
                self.book.close()

    def create_sheets(self, sheets_name: list[str] = None):
        if self.book and sheets_name:
            for name in sheets_name:
                self.book.create_sheet(name)

    def set_sheet_grid(self, grid: bool = True):
        if self.book and self.sheet:
            self.sheet.sheet_view.showGridLines = grid
