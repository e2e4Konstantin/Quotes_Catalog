from catalog import catalog_fill, catalog_none_check
from read_quotes_parametes import read_parameters, free_data_bank
from read_quotes_parametes.common_data import data_bank
from excelutils import write_to_excel


def application():
    catalog = catalog_fill()
    # catalog.info()
    catalog.details_info()
    print(f"<< {'-' * 50} >>\n")
    # catalog_none_check(catalog)
    # print(f"<< {'-' * 50} >>\n")
    read_parameters(catalog)
    print(data_bank.keys())
    free_data_bank()



    # write_to_excel(catalog)



if __name__ == "__main__":
    application()
