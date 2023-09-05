import os
from settings import Catalog
from filesutils import get_full_file_name, does_file_in_use, out_error_message_and_exit
from excelutils.data_out_to_excel import data_out_to_excel


def write_to_excel(catalog: Catalog = None):
    path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\Quote_Catalog\output"
    file = r"output_template.xlsx"
    full_name = get_full_file_name(file, path)
    if full_name and os.path.isfile(full_name):
        if not does_file_in_use(full_name):
            os.remove(full_name)
        else:
            out_error_message_and_exit(f"этот файл занят другим приложением: ", full_name)
    elif os.path.isdir(path):
        print(full_name)
    else:
        out_error_message_and_exit(f"нет такой папки: ", path)
    data_out_to_excel(catalog, full_name)
