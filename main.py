from catalog import read_catalog


def application():
    # path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\Quote_Catalog\src"
    path = r"C:\Users\kazak.ke\PycharmProjects\Quotes_Catalog\src"
    file = r"catalog_3.xlsx"
    sheet = 'catalog'
    read_catalog(file, path, sheet)
    write_catalog()


if __name__ == "__main__":
    application()
