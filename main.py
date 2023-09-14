import os
from catalog import catalog_fill, catalog_none_check
from read_quotes_parametes import read_parameters, free_data_bank
from read_quotes_parametes.common_data import data_bank
from excelutils import data_out_to_excel
from filesutils import location

from settings import Catalog



loc = {1: "home", 2: "office"}


def application():
    catalog_file, catalog_json, parameterization_file = location(loc[2])
    catalog = catalog_fill(catalog_file, catalog_json)
    catalog.info()
    catalog.details_info()
    print(f"<< {'-' * 50} >>\n")
    # catalog_none_check(catalog)
    # print(f"<< {'-' * 50} >>\n")
    read_parameters(catalog, src_file=parameterization_file)
    print(data_bank.keys())
    print(f"<< {'-' * 50} >>\n")
    # free_data_bank()

    data_out_to_excel(catalog, parameterization_file)


if __name__ == "__main__":
    application()
