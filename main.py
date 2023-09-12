import os
from catalog import catalog_fill, catalog_none_check
from read_quotes_parametes import read_parameters, free_data_bank
from read_quotes_parametes.common_data import data_bank
from excelutils import write_to_excel
from filesutils import location






def application():
    catalog_file, catalog_json, parameterization_file = location("office")
    catalog = catalog_fill(catalog_file, catalog_json)
    catalog.info()
    catalog.details_info()
    print(f"<< {'-' * 50} >>\n")
    # catalog_none_check(catalog)
    # print(f"<< {'-' * 50} >>\n")
    read_parameters(catalog, src_file=parameterization_file)
    print(data_bank.keys())
    print(f"<< {'-' * 50} >>\n")
    free_data_bank()

    write_to_excel(catalog)


if __name__ == "__main__":
    application()
