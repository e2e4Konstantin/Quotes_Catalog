import sys
import pandas
import gc
from filesutils import get_full_file_name
from settings import console_colors


class SourceData:
    def __init__(self, data_frame_name: str = None, file_name: str = None, file_path: str = None,
                 sheet_name: str = None, skip_rows: int = 0, what_columns=None):
        # -- dataframe
        self.name = data_frame_name if data_frame_name and len(data_frame_name) > 0 else None
        self.df: pandas.DataFrame() = None  # ссылка на массив данных
        self.row_max = 0                    # максимальный индекс строки
        self.column_max = 0                 # максимальный индекс колонки
        # -- читаем данные из файла excel в массив
        self.get_data_from_excel(file_name, file_path, sheet_name, skip_rows, what_columns)

    def get_data_from_excel(self, file_name: str = None, file_path: str = None, sheet_name: str = None,
                            skip_rows: int = 0, what_columns=None):
        full_name = get_full_file_name(file_name, file_path)
        if full_name:
            try:
                self.df = pandas.read_excel(io=full_name, sheet_name=sheet_name,
                                            usecols=what_columns,   # список столбцов "A:D"
                                            header=None,            # не читать заголовок
                                            dtype="object",
                                            skiprows=skip_rows)
                if not self.df.empty:
                    self.row_max = self.df.shape[0] - 1
                    self.column_max = self.df.shape[1] - 1
                    print(f"данные прочитаны из файла: {full_name}, лист: '{sheet_name}'.")
                else:
                    raise TypeError(self.__class__)
            except Exception as err:
                error_out = f"{console_colors['RED']}{err}{console_colors['RESET']}"
                show_full_name = f"'{console_colors['YELLOW']}{full_name}{console_colors['RESET']}'"
                print(f"ошибка при чтении данных из файла {show_full_name}:\n\t-->> {error_out}")
                sys.exit()
        else:
            show_full_name = f"'{console_colors['YELLOW']}{full_name}{console_colors['RESET']}'"
            print(f"Не найден excel файл с данными {show_full_name}.")
            sys.exit()

    def __str__(self):
        return f"название массива данных: '{self.name}'\nстрок: {self.row_max + 1}, столбцов: {self.column_max + 1}\n" \
               f"pandas.version: {pandas.__version__}"

    def set_columns_name_type_column_data(self, names: list[str], changed_types: dict[str: type] = None):
        if names:
            self.df.columns = names
            # print(self.df.dtypes)
            # print(self.df.columns)
        if changed_types:
            self.df = self.df.astype(changed_types)
            # print(self.df.info())

    def delete_columns_by_index(self, indexes: list[int]):
        self.df.drop(self.df.columns[indexes], axis=1, inplace=True)
        # print(self.df.columns)

    def delete_columns_by_names(self, names: list[str]):
        self.df.drop(names, axis=1, inplace=True)
        # print(self.df.columns)

    def get_cell_str_value(self, row, column) -> str:
        # value: str = "" if pd.isnull(tmp_val) else tmp_val
        if row >= 0 and column >= 0:
            src_value = self.df.iat[row, column]
            if pandas.isna(src_value):
                return ""
            match src_value:
                case int() | float():
                    return str(src_value)
                case str():
                    return " ".join(src_value.split())
                case _:
                    return str(src_value or "").strip()
        return ""

    def printing_dataset_information(self):
        print(f"{self.df.info(verbose=False, show_counts=False) = }")
        print(f"{self.df.index}")
        print(f"{self.df.head(3)}")
        # print(f"{self.df.memory_usage(index=True, deep=True)}")
        print(f"memory: {self.df.memory_usage(index=True, deep=True).sum()} bytes")
        print(f"{self.df.columns.values.tolist()}")
        # print(f"{[*self.df]}")
        # df_set = {*self.df}
        # print(f"{df_set = }")
        # print(f"{*self.df, = }")


if __name__ == "__main__":
    # path = r"C:\Users\kazak.ke\PycharmProjects\Quotes_Parsing\output"
    path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\Quote_Catalog\src"
    file = r"template_all_output.xlsx"
    sheet = r"Tables"
    data = SourceData("T", file, path, sheet, skip_rows=1)
    print(data)
    t = ["row", "show", "numb", "atr_c", "par_c", "name", "atr", "par"]
    types = {"show": str, "numb": str, 'atr_c': int, 'par_c': int, "name": str}
    data.set_columns_name_type_column_data(t, types)
    data.delete_columns_by_names(["row", ])
    print(data.df.info())

    del data
    gc.collect()

