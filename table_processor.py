# table_processor.py

class TableProcessor:
    def __init__(self):
        self.current_table_data = None  # Переменная для хранения текущих данных таблицы

    def process(self, table_name, raw_data, table_widget):
        """
        Направляет обработку выбранной таблицы в соответствующий обработчик.

        :param table_name: Название таблицы
        :param raw_data: Полные сырые данные DAT-файла
        :param table_widget: Виджет таблицы для отображения данных
        :return: Результат обработки таблицы
        """
        if table_name == "Паспорт коровы или телки":
            from table_000005_processor import Table000005Processor
            processor = Table000005Processor()
            return processor.process_table(raw_data, table_widget)
        
        if table_name == "Перемещение животного":
            from table_000006_processor import Table000006Processor
            processor = Table000006Processor()
            return processor.process_table(raw_data, table_widget)

        if table_name == "Результат контрольной дойки":
            from table_000007_processor import Table000007Processor
            processor = Table000007Processor()
            return processor.process_table(raw_data, table_widget)        

        if table_name == "Взвешивание":
            from table_000008_processor import Table000008Processor
            processor = Table000008Processor()
            return processor.process_table(raw_data, table_widget)

        if table_name == "Осеменение":
            from table_000009_processor import Table000009Processor
            processor = Table000009Processor()
            return processor.process_table(raw_data, table_widget)

        if table_name == "Проверка на стельность":
            from table_000010_processor import Table000010Processor
            processor = Table000010Processor()
            return processor.process_table(raw_data, table_widget)

        if table_name == "Отел":
            from table_000011_processor import Table000011Processor
            processor = Table000011Processor()
            return processor.process_table(raw_data, table_widget)

        if table_name == "Аборт":
            from table_000012_processor import Table000012Processor
            processor = Table000012Processor()
            return processor.process_table(raw_data, table_widget)

        if table_name == "Запуск":
            from table_000013_processor import Table000013Processor
            processor = Table000013Processor()
            return processor.process_table(raw_data, table_widget)
			
        if table_name == "Выбытие":
            from table_000014_processor import Table000014Processor
            processor = Table000014Processor()
            return processor.process_table(raw_data, table_widget)
			
        if table_name == "Охота":
            from table_000015_processor import Table000015Processor
            processor = Table000015Processor()
            return processor.process_table(raw_data, table_widget)			

        # Если обработчик для таблицы не найден, возвращаем сообщение об отсутствии обработки
        return f"Обработчик для таблицы '{table_name}' не реализован."