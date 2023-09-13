import os
def get_full_file_name(file_name: str, file_path: str = "") -> str | None:
    """ Создает путь к файлу из файла и маршрута. Проверяет что этот путь корректный """
    if file_name and file_path:
        splicing = os.path.normpath(os.path.join(file_path, file_name))
        if os.path.isabs(splicing):
            return splicing
        print("*********")
    return None




f = r'f:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\Quote_Catalog\src\template_3_68_output.xlsx'
path, file = os.path.split(f)
output_file = f"renew_{file}"
print(get_full_file_name(output_file, path))


#
#
# p = os.getcwd()
# print(p, os.path.isabs(p))
# path, file = os.path.split(f)
# path = os.path.normpath(path)
# cuts_path = os.path.split(path)
# print(cuts_path)
#
# dd= os.path.normpath(os.path.join(*cuts_path, "output"))
# print(dd)
#
#
# output_file = f"renew_{file}"
# full_name = os.path.join(dd, output_file)

#
# print(full_name)
# print(os.path.isabs(full_name))
# print(os.path.normpath(full_name))
#
# full_name = os.path.normpath(full_name)
# print(os.path.isabs(full_name))
#
# x = os.path.abspath(os.path.expanduser(os.path.expandvars(f)))
# print(x)
# print(os.path.isabs(x))
#
#


# print(os.path.abspath(__file__))

# original_path = os.getcwd()
# print(os.getcwd())
# os.chdir(path)
# print(os.getcwd())
# os.chdir(original_path ) # here is the restore of the original path
# print(os.getcwd())