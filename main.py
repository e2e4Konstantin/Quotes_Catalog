from catalog import catalog_fill, catalog_none_check
from excelutils import write_to_excel


def application():
    catalog = catalog_fill()
    catalog.info()
    print(f"<< {'-' * 50} >>\n")
    # catalog_none_check(catalog)
    # print(f"<< {'-' * 50} >>\n")
    write_to_excel(catalog)


if __name__ == "__main__":
    application()
