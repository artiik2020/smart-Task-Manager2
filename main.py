import io
import sys
import sqlite3
import shutil

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog


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
    <width>798</width>
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
   <widget class="QWidget" name="layoutWidget">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>420</y>
      <width>401</width>
      <height>164</height>
     </rect>
    </property>
    <layout class="QFormLayout" name="formLayout">
     <item row="0" column="1">
      <widget class="QPushButton" name="pushButton_4">
       <property name="enabled">
        <bool>true</bool>
       </property>
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
        <string>Удалить дело</string>
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
   <widget class="QWidget" name="">
    <property name="geometry">
     <rect>
      <x>400</x>
      <y>420</y>
      <width>391</width>
      <height>141</height>
     </rect>
    </property>
    <layout class="QVBoxLayout" name="verticalLayout">
     <item>
      <widget class="QPushButton" name="pushButton_2">
       <property name="text">
        <string>Импортировать задачи</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="pushButton_6">
       <property name="text">
        <string>Экспортировать задачи</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="pushButton_5">
       <property name="text">
        <string>сделать тёмную тему</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="pushButton_7">
       <property name="text">
        <string>установить дату и времея напоминания</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QDateTimeEdit" name="dateTimeEdit"/>
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
     <width>798</width>
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
        self.pushButton_2.clicked.connect(self.add_base)
        self.pushButton_6.clicked.connect(self.load_base)

    def setup_table(self):
        """работает"""
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('tasks.db')

        if not self.db.open():
            raise Db_not_open

        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('tasks_table')
        self.model.select()
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "Задача")
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        self.tableView.show()

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks_table (
                tasks NUMERIC UNIQUE NOT NULL
            )
        ''').fetchall()

        self.cur.execute('''
            INSERT OR IGNORE INTO tasks_table (tasks) 
            VALUES ('Важное дело')
        ''').fetchall()
        self.save_data()

    def delete_task(self):
        """Работает(наконец-то)"""
        selected_indexes = self.tableView.selectedIndexes()
        if selected_indexes:
            try:
                selected_row = selected_indexes[0].row()
                task_id = self.model.data(self.model.index(selected_row, 0))
                self.cur.execute('DELETE FROM tasks_table WHERE tasks = ?', (task_id,))
                self.con.commit()
                self.model.select()

                self.model.select()
            except Exception as e:
                print(f"Ошибка удаления: {e}")
        self.save_data()

    def new_cattegory(self):
        """работает"""
        line_text = self.lineEdit_2.text()
        try:
            if line_text != '':
                self.cur.execute(f'ALTER TABLE tasks_table ADD COLUMN {line_text} NUMERIC').fetchall()
                self.save_data()
            else:
                self.statusBar().showMessage('Поле пустое')
        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e}')

    def create_task(self):
        """работает"""
        line_text = self.lineEdit.text()
        if line_text != '':
            record = self.model.record()
            record.setValue("tasks", line_text)
            if self.model.insertRecord(-1, record):
                self.lineEdit.clear()
                self.statusBar().showMessage('Успешно добавлено!')
                self.save_data()
            else:
                self.statusBar().showMessage('Ошибка при добавлении задачи')
        else:
            self.statusBar().showMessage('Поле пустое')

    def add_base(self):
        try:
            file_name = 'tasks.db'
            path = QFileDialog.getSaveFileName(self, caption='Сохранить файл',
                                               directory='tasks.db',
                                               filter='All Files')
            shutil.copy(file_name, path[0])
        except Exception as e:
            print(e)

    def save_data(self):
        '''сохранение данных в таблицу'''
        self.con.commit()
        self.tableView.setModel(None)
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('tasks_table')
        self.model.select()
        self.tableView.setModel(self.model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimplePlanner()
    window.show()
    sys.exit(app.exec())
