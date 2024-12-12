# dat_reader.py

import chardet

class DatReader:
    def read(self, file_path):
        """
        Читает содержимое DAT-файла и возвращает его как строку с учётом автоматического определения кодировки.

        :param file_path: Путь к DAT-файлу
        :return: Содержимое файла в виде строки
        """
        try:
            # Сначала читаем файл в байтовом режиме
            with open(file_path, 'rb') as file:
                raw_data = file.read()

            # Определяем кодировку файла
            detected = chardet.detect(raw_data)
            encoding = detected['encoding']
            print(f"Определённая кодировка: {encoding}")

            # Декодируем файл с использованием найденной кодировки
            data = raw_data.decode(encoding, errors='replace')
            return data
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")
            return None
