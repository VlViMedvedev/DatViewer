from tables_reference import TABLES_REFERENCE
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QTableWidgetItem

class Table000013Processor:
    def process_table(self, raw_data, table_widget):
        """
        Обрабатывает таблицу 000013 (Запуск) и отображает её в табличной части интерфейса.

        :param raw_data: Полные сырые данные DAT-файла
        :param table_widget: Виджет таблицы для отображения данных
        :return: Кортеж: сырые данные для отображения и сообщение об ошибках
        """
        print("Начата обработка таблицы 000013")
        table_code = "000013"
        table_lines = []
        inside_table = False

        # Извлечение данных таблицы из сырых данных
        for line in raw_data.splitlines():
            if line.startswith("DN") and table_code in line:
                print(f"Найдена строка DN: {line}")
                inside_table = True
                dn_line = line  # Сохраняем строку DN
            elif line.startswith("VN") and inside_table and line.startswith(f"VN{table_code}"):
                print(f"Найдена строка VN: {line}")
                table_lines.append(line)  # Добавляем строки VN
            elif line.startswith("TN") and inside_table:
                print(f"Найдена строка TN, завершение блока таблицы 000013")
                inside_table = False  # Завершаем сбор таблицы

        if not table_lines:
            print(f"Данные для таблицы {table_code} не найдены.")
            return "", f"Данные для таблицы {table_code} не найдены."

        # Парсим строку DN для получения описания полей
        fields_description = self.parse_dn_line(dn_line)
        
        if not fields_description:
            print("Не удалось распарсить описание полей из строки DN.")
            return dn_line, "Ошибка разбора описания полей."

        # Настройка столбцов в таблице
        table_widget.clear()
        table_widget.setColumnCount(len(fields_description))
        table_widget.setRowCount(len(table_lines))

        # Установка заголовков с жирным шрифтом для M и K
        for col, field in enumerate(fields_description):
            header_text = f"{field['type']} {field['code']} ({self.get_field_name(field['code'])})".strip()
            header_item = QTableWidgetItem(header_text)
            if field["type"] in ("M", "K"):
                font = QFont()
                font.setBold(True)
                header_item.setFont(font)
            table_widget.setHorizontalHeaderItem(col, header_item)

        print("Начинается разбор строк VN...")
        # Анализ строк VN
        errors = []
        for row, vn_line in enumerate(table_lines, start=1):  # Нумерация начинается с 1
            print(f"Разбор строки VN ({row}): {vn_line}")
            column_data = self.parse_vn_line(vn_line, fields_description, errors, row)
            for col, (value, field) in enumerate(zip(column_data, fields_description)):
                item = QTableWidgetItem(value)
                # Проверка на тип поля и содержимое
                if field["type"] in ("K", "M") and value.strip() == "?" * field["length"]:
                    item.setBackground(QColor("red"))  # Красный фон для ячейки
                table_widget.setItem(row - 1, col, item)  # row - 1 для индекса таблицы

        print("Обработка завершена.")
        return dn_line + "\n" + "\n".join(table_lines), "\n".join(errors)

    def parse_dn_line(self, dn_line):
        """
        Разбирает строку DN и возвращает описание полей.

        :param dn_line: Строка DN
        :return: Список словарей с описанием полей
        """
        print("Подробный разбор строки DN:")
        fields = []
        start = 8  # Пропускаем "DN000013"
        while start < len(dn_line):
            block = dn_line[start:start + 11]
            if len(block) < 11:
                print(f"Неполный блок данных: {block}")
                break

            field = {
                "prefix": block[:2],
                "code": block[2:8],
                "length": int(block[8:10]),
                "precision": int(block[10:11]),
                "type": self.get_field_type(block[2:8]),
            }
            fields.append(field)
            print(f"  Поле: {field}")
            start += 11

        return fields

    def parse_vn_line(self, vn_line, fields_description, errors, row_number):
        """
        Парсит строку VN на основе описания полей из DN.

        :param vn_line: Строка VN
        :param fields_description: Описание полей из DN
        :param errors: Список для записи ошибок
        :param row_number: Номер текущей строки (начиная с 1)
        :return: Список значений для отображения в таблице
        """
        result = []
        start = 8  # Пропускаем "VN000013"

        for field in fields_description:
            length = field["length"]
            value = vn_line[start:start + length].strip()

            if field["type"] in ("K", "M") and value == "?" * length:
                field_name = self.get_field_name(field["code"])
                errors.append(
                    f"Для строки №{row_number} не заполнено обязательное поле {field['code']} ({field_name})"
                )

            result.append(value)
            start += length

        return result

    def get_field_type(self, code):
        for field in TABLES_REFERENCE.get("DD000013", []):
            if field["code"] == code:
                return field.get("type", "")
        return ""

    def get_field_name(self, code):
        for field in TABLES_REFERENCE.get("DD000013", []):
            if field["code"] == code:
                return field["name"]
        return "Неизвестное поле"
