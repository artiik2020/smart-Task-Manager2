import io
import sys
import sqlite3

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow

class Db_not_open():
    pass

tempalte = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QTableView" name="tableView">
    <property name="geometry">
     <rect>
      <x>5</x>
      <y>11</y>
      <width>791</width>
      <height>411</height>
     </rect>
    </property>
   </widget>
   <widget class="QWidget" name="">
    <property name="geometry">
     <rect>
      <x>60</x>
      <y>420</y>
      <width>661</width>
      <height>135</height>
     </rect>
    </property>
    <layout class="QFormLayout" name="formLayout">
     <item row="0" column="1">
      <widget class="QPushButton" name="pushButton_4">
       <property name="text">
        <string>Создать</string>
       </property>
      </widget>
     </item>
     <item row="1" column="1">
      <widget class="QLineEdit" name="lineEdit">
       <property name="placeholderText">
        <string>Для создания нового дела напишите название</string>
       </property>
      </widget>
     </item>
     <item row="2" column="1">
      <widget class="QPushButton" name="pushButton_3">
       <property name="text">
        <string>Удалить все дела</string>
       </property>
      </widget>
     </item>
     <item row="3" column="1">
      <widget class="QPushButton" name="pushButton">
       <property name="maximumSize">
        <size>
         <width>16777215</width>
         <height>23</height>
        </size>
       </property>
       <property name="text">
        <string>Новая категория</string>
       </property>
      </widget>
     </item>
     <item row="4" column="1">
      <widget class="QLineEdit" name="lineEdit_2">
       <property name="placeholderText">
        <string>Для создания новой категории напишите здесь название </string>
       </property>
      </widget>
     </item>
    </layout>
   </widget>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>

'''


class SimplePlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(tempalte)
        uic.loadUi(f, self)
        self.con = sqlite3.connect('tasks.db')
        self.cur = self.con.cursor()
        self.setup_table()

        self.pushButton_4.clicked.connect(self.create_task)
        self.pushButton.clicked.connect(self.new_cattegory)
        self.pushButton_3.clicked.connect(self.delete_task)

    def setup_table(self):
        # 1. Подключение к БД
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('tasks.db')

        if not self.db.open():
            raise Db_not_open

        # 2. Создание модели
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('tasks_table')

        # 3. Загрузка данных
        self.model.select()

        # 4. Настройка заголовков
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "Задача")

        # 5. Связывание с таблицей
        self.tableView.setModel(self.model)

        # 6. Настройка отображения
        self.tableView.resizeColumnsToContents()
        self.tableView.show()


    def delete_task(self):
        self.model.clear()
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "Задача")
        self.model.select()

    def new_cattegory(self):
        count_col = self.model.columnCount()
        line_text = self.lineEdit_2.text()
        self.model.setHeaderData(count_col + 1, Qt.Orientation.Horizontal, line_text)
        self.model.select()

    def create_task(self):
        pass

    def load_file(self):
        self.model.submitAll()

    def process_data(self):
        self.model.submitAll()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimplePlanner()
    window.show()
    sys.exit(app.exec())
