import time
from excelutils.excel_tools_setting import ExcelControl
from excelutils.templates import (
    styles_add, create_basic_header,
    put_table_to_sheet, put_quote_to_sheet, put_attributes_to_sheet, put_parameters_to_sheet
)
from datautils import (
    get_all_tables_from_data,
    get_all_quotes_for_tables_from_data_by_index,
    get_all_attributes_for_quote_from_data_by_index,
    get_all_parameters_for_quote_from_data_by_index
)


def data_out_to_excel(file_name: str = None, file_path: str = None, sheets_name: list[str] = None, grid: bool = True):
    """ Подготовка выходного файла. Удаляет все содержимое и создает шапку таблицы. """
    output_file = ExcelControl(file_name, file_path)
    with output_file as ex:
        ex.delete_all_sheets()
        ex.create_sheets(sheets_name)
        print(output_file)

        styles_add(ex.book)
        ex.sheet = ex.book['name']
        ex.set_sheet_grid(grid=grid)
        create_basic_header(ex.sheet)

        ex.sheet.sheet_properties.outlinePr.summaryBelow = False    # группировка сверху

        start_table_row = 6
        step_table_row = 2
        table_row = start_table_row

        # прочитать данные о всех таблицах
        tables = get_all_tables_from_data()
        for table in tables:
            table_time = time.monotonic()
            table_cod = table[0]
            quotes = get_all_quotes_for_tables_from_data_by_index(table_cod)
            if len(quotes) > 0:
                put_table_to_sheet(ex.sheet, table, table_row)
                quote_row = table_row+1
                for quote in quotes:
                    quote_cod = quote[2]
                    put_quote_to_sheet(ex.sheet, quote, quote_row)
                    attributes = get_all_attributes_for_quote_from_data_by_index(quote_cod)   # получаем атрибуты для расценки из датасета
                    table_attributes = table[2]
                    put_attributes_to_sheet(ex.sheet, attributes, quote_row, table_attributes)

                    table_parameters = table[3]
                    parameters = get_all_parameters_for_quote_from_data_by_index(quote_cod)  # получаем параметры для расценки из датасета

                    attribute_counter = len([x.strip() for x in table_attributes.split(',')])
                    put_parameters_to_sheet(ex.sheet, parameters, quote_row, table_parameters, attribute_counter)

                    quote_row += 1
                table_row = quote_row + step_table_row
                delta_time = time.monotonic() - table_time
                print(f"\tвремя обработки таблицы '{table_cod :<15s}': {f'{delta_time :0.4f}' :>10s} сек.")

