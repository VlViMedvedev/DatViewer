# main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui import GUI
from dat_reader import DatReader
from dat_parser import DatParser
from table_processor import TableProcessor

def main():
    # Создаём экземпляр QApplication
    app = QApplication(sys.argv)

    # Инициализация компонентов
    dat_reader = DatReader()
    dat_parser = DatParser()
    table_processor = TableProcessor()

    # Создание GUI
    gui = GUI(dat_reader, dat_parser, table_processor)
    gui.show()

    # Запуск цикла событий
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
