from read_quotes_parametes.common_data import data_bank


def get_table_from_data(row) -> tuple[str, str, str, str]:
    """ Получает кортеж информации по таблице из dataset. """
    cod = data_bank["tables"].get_cell_str_value(row, 1)
    title = data_bank["tables"].get_cell_str_value(row, 4)
    attributes = data_bank["tables"].get_cell_str_value(row, 5)
    parameters = data_bank["tables"].get_cell_str_value(row, 6)
    return cod, title, attributes, parameters


def get_all_tables_from_data() -> list[tuple[str, str, str, str]]:
    # ['number', 'table_name', 'attributes', 'parameters']
    tables_list = []
    # убираем индекс
    [tables_list.append(tables[1:]) for tables in data_bank["tables"].df.to_records().tolist()]
    # print(tables_list)
    return tables_list


def get_all_quotes_for_tables_from_data_by_index(table_cod: str) -> list:
    # quotes_list: list[QuoteInfo] = []
    quotes = data_bank["quotes"]
    # ["table", "cod", "title", "measure", "stat", "flag", "basic_slave", "link_cod"]
    quotes_for_table = quotes.df.loc[quotes.df["table"] == table_cod]
    quotes_list = quotes_for_table.to_records().tolist()
    # print(quotes_list)
    return quotes_list


def get_all_attributes_for_quote_from_data_by_index(quote_cod: str) -> list:
    # column_names = ["quote", "name", "value"]
    attributes = data_bank["attributes"]
    quote_attributes = attributes.df.loc[attributes.df["quote"] == quote_cod]
    attributes_list = quote_attributes.to_records().tolist()
    # print(attributes_list)
    return attributes_list


def get_all_parameters_for_quote_from_data_by_index(quote_cod: str) -> dict:
    # column_names = ["quote", "name", "left", "right", "measure", "step", "type"]
    parameters = data_bank["parameters"]

    quote_parameters = parameters.df.loc[parameters.df["quote"] == quote_cod]
    parameters_list = quote_parameters.to_records().tolist()
    # print(parameters_list)
    return parameters_list
