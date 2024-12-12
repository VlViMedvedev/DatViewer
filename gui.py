from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton, 
                             QFileDialog, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QLabel, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QTextCharFormat, QColor
from tables_reference import TABLES_REFERENCE

class GUI(QMainWindow):
    def __init__(self, dat_reader, dat_parser, table_processor):
        super().__init__()
        
        self.dat_reader = dat_reader
        self.dat_parser = dat_parser
        self.table_processor = table_processor
        self.raw_data = None  # Переменная для хранения полного сырого содержимого файла

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("DAT File Checker")
        self.setGeometry(100, 100, 800, 600)

        # Главное окно
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной макет
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Кнопка для загрузки файла
        self.load_button = QPushButton("Загрузить DAT файл")
        self.load_button.clicked.connect(self.load_file)
        main_layout.addWidget(self.load_button)

        # Поле фильтрации
        self.filter_input = QTextEdit()
        self.filter_input.setPlaceholderText("Введите текст для фильтрации...")
        self.filter_input.setFixedHeight(30)
        self.filter_input.textChanged.connect(self.apply_filter)
        main_layout.addWidget(self.filter_input)

        # Разделитель для интерфейса
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Левое меню: список таблиц
        self.table_list_widget = QListWidget()
        self.table_list_widget.setFont(QFont("Arial", 6))  # Уменьшенный шрифт
        self.table_list_widget.setMinimumWidth(50)  # Минимальная ширина
        self.table_list_widget.setMaximumWidth(200)  # Максимальная ширина
        self.table_list_widget.itemClicked.connect(self.on_table_selected)  # Обработчик клика
        splitter.addWidget(self.table_list_widget)

        # Установить пропорции растяжения
        splitter.setStretchFactor(0, 1)  # Левая часть минимально растягивается
        splitter.setStretchFactor(1, 4)  # Правая часть занимает больше пространства

        # Инициализация меню в неактивном состоянии
        self.populate_menu()

        # Правая часть: таблица и содержимое
        right_widget = QSplitter(Qt.Vertical)  # Вертикальный разделитель для правой части
        splitter.addWidget(right_widget)

        # Таблица
        table_widget_container = QWidget()
        table_layout = QVBoxLayout()
        table_widget_container.setLayout(table_layout)
        self.table_widget = QTableWidget()
        table_layout.addWidget(self.table_widget)
        right_widget.addWidget(table_widget_container)

        # Сырое содержимое
        raw_content_container = QWidget()
        raw_content_layout = QVBoxLayout()
        raw_content_container.setLayout(raw_content_layout)
        self.raw_content = QTextEdit()
        self.raw_content.setReadOnly(True)
        self.raw_content.setFont(QFont("Courier", 10))  # Устанавливаем моноширинный шрифт
        raw_content_layout.addWidget(QLabel("Сырое содержимое файла"))
        raw_content_layout.addWidget(self.raw_content)
        right_widget.addWidget(raw_content_container)

        # Окно для ошибок
        error_log_container = QWidget()
        error_log_layout = QVBoxLayout()
        error_log_container.setLayout(error_log_layout)
        self.error_log = QTextEdit()
        self.error_log.setReadOnly(True)
        error_log_layout.addWidget(QLabel("Ошибки"))
        error_log_layout.addWidget(self.error_log)
        right_widget.addWidget(error_log_container)

    def load_file(self):
        # Открытие диалога для выбора файла
        file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать DAT файл", "", "DAT Files (*.dat)")
        if file_name:
            print(f"Файл выбран: {file_name}")
            data = self.dat_reader.read(file_name)
            if data:
                self.raw_data = data  # Сохраняем полные данные файла
                self.process_data(data)

    def process_data(self, data):
        # Разбор файла
        self.raw_content.clear()
        self.error_log.clear()

        # Отображение сырого содержимого напрямую
        self.raw_content.setText(data)

        table_data = self.dat_parser.parse(data)

        # Обновление списка в левой части
        for i in range(self.table_list_widget.count()):
            item = self.table_list_widget.item(i)
            table_name = item.text().split(" (")[0]  # Извлекаем имя таблицы без счётчика

            if table_name in table_data:
                vn_count = table_data[table_name]
                item.setText(f"{table_name} ({vn_count})")  # Добавляем количество строк VN
                item.setFlags(Qt.ItemIsEnabled)  # Делаем строку активной
            else:
                item.setText(table_name)  # Оставляем только название таблицы
                item.setFlags(Qt.NoItemFlags)  # Оставляем строку неактивной

    def on_table_selected(self, item):
        # Обработчик выбора таблицы в левой части
        table_name = item.text().split(" (")[0]  # Получаем имя таблицы без счётчика
        if self.raw_data:
            raw_data, errors = self.table_processor.process(table_name, self.raw_data, self.table_widget)
            self.raw_content.setText(raw_data)  # Отображаем сырые данные
            self.error_log.setText(errors)  # Отображаем ошибки

    def apply_filter(self):
        """Фильтрация таблицы и подсветка совпадений в сыром содержимом."""
        filter_text = self.filter_input.toPlainText()
        
        # Фильтрация таблицы
        for row in range(self.table_widget.rowCount()):
            match_found = False
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item and filter_text.lower() in item.text().lower():
                    match_found = True
                    break
            self.table_widget.setRowHidden(row, not match_found)

        # Подсветка совпадений в сыром содержимом
        self.highlight_matches(filter_text)

    def highlight_matches(self, text):
        """Подсветка совпадений текста в сыром содержимом."""
        cursor = self.raw_content.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())  # Сбрасываем форматирование
        cursor.clearSelection()

        if text:
            # Формат для подсветки
            highlight_format = QTextCharFormat()
            highlight_format.setBackground(QColor("yellow"))

            # Поиск совпадений
            cursor = self.raw_content.textCursor()
            while not cursor.isNull() and not cursor.atEnd():
                cursor = self.raw_content.document().find(text, cursor)
                if cursor.isNull():
                    break
                cursor.mergeCharFormat(highlight_format)

    def populate_menu(self):
        # Заполнение меню из справочника Event (все пункты неактивны до загрузки файла)
        events = TABLES_REFERENCE.get("Event", {})
        for key, name in events.items():
            item = QListWidgetItem(name)  # Создание элемента списка
            item.setFlags(Qt.NoItemFlags)  # Делаем элемент неактивным
            self.table_list_widget.addItem(item)  # Добавление элемента в список

if __name__ == "__main__":
    import sys
    from dat_reader import DatReader
    from dat_parser import DatParser
    from table_processor import TableProcessor

    app = QApplication(sys.argv)

    # Инициализация заглушек для логики
    dat_reader = DatReader()
    dat_parser = DatParser()
    table_processor = TableProcessor()

    gui = GUI(dat_reader, dat_parser, table_processor)
    gui.show()

    sys.exit(app.exec_())
