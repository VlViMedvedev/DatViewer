# dat_parser.py

from tables_reference import TABLES_REFERENCE

class DatParser:
    def parse(self, raw_data):
        """
        Парсит содержимое DAT-файла и возвращает список таблиц с количеством строк VN.

        :param raw_data: Содержимое DAT-файла в виде строки
        :return: Словарь вида {"Название таблицы": количество VN строк}
        """
        tables = {}  # Словарь для хранения таблиц и количества VN строк

        # Разделяем файл на строки
        lines = raw_data.splitlines()

        current_table_code = None
        vn_count = 0

        for line in lines:
            # Ищем строки, начинающиеся с DN
            if line.startswith("DN"):
                # Если есть текущая таблица, сохраняем её количество VN строк
                if current_table_code is not None and vn_count > 0:
                    table_name = TABLES_REFERENCE["Event"].get(current_table_code, f"Неизвестная таблица ({current_table_code})")
                    tables[table_name] = vn_count

                # Обновляем текущую таблицу и сбрасываем счётчик VN строк
                current_table_code = line[2:8]  # Код таблицы из строки DN (6 символов после DN)
                vn_count = 0

            # Считаем строки VN для текущей таблицы
            elif line.startswith("VN") and current_table_code is not None:
                vn_count += 1

        # Сохраняем последнюю таблицу, если она есть
        if current_table_code is not None and vn_count > 0:
            table_name = TABLES_REFERENCE["Event"].get(current_table_code, f"Неизвестная таблица ({current_table_code})")
            tables[table_name] = vn_count

        return tables