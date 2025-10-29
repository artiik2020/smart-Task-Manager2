import io
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(tempalte)
        uic.loadUi(f, self)

        menu_bar = self.menuBar()

        # Меню «Файл»
        file_menu = menu_bar.addMenu("Файл")

        # Действия
        open_action = file_menu.addAction("Открыть файл")
        save_action = file_menu.addAction("Сохранить")
        exit_action = file_menu.addAction("Выход")

        # Подключаем
        open_action.triggered.connect(self.load_file)
        save_action.triggered.connect(self.process_data)
        exit_action.triggered.connect(self.close)

        edit_menu = menu_bar.addMenu("редактирование")
        sub_menu = edit_menu.addMenu("Подменю категорий")
        sub_menu.addAction("Удалить")
        sub_menu.addAction("Создать")

    def load_file(self):
        pass

    def process_data(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
