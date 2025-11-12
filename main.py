import io
import sys
import sqlite3
import shutil

from PyQt6 import uic
from PyQt6.QtCore import Qt, QDateTime, QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QSystemTrayIcon, QStyle, QMenu
from plyer import notification


class Db_not_open():
    pass


dark_style = '''
QMainWindow, QWidget {
    background-color: #2d2d2d;
    color: #e0e0e0;
}
QTableView {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 2px solid #404040;
    font-size: 14px;
    gridline-color: #404040;
}


QMainWindow {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QWidget {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QTableView {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 2px solid #404040;
    font-size: 14px;
    gridline-color: #404040;
    outline: none;
}

QTableView::item {
    background-color: #2d2d2d;
    color: #e0e0e0;
    padding: 8px;
    border-bottom: 1px solid #404040;
    min-height: 25px;
}

QTableView::item:selected {
    background-color: #4CAF50;
    color: #ffffff;
}

QTableView::item:hover {
    background-color: #3d3d3d;
}

QHeaderView {
    background-color: #404040;
    color: #e0e0e0;
}

QHeaderView::section {
    background-color: #404040;
    color: #e0e0e0;
    padding: 8px;
    border: 1px solid #2d2d2d;
    font-weight: bold;
    font-size: 14px;
    min-height: 30px;
}

QTableCornerButton::section {
    background-color: #404040;
    border: 1px solid #2d2d2d;
}

QPushButton {
    background-color: #4CAF50;
    color: #ffffff;
    border: none;
    padding: 10px 16px;
    font-size: 14px;
    border-radius: 4px;
    min-height: 20px;
    min-width: 120px;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b40;
}

QPushButton#pushButton_3,
QPushButton#pushButton_6, 
QPushButton#pushButton_2, 
QPushButton#pushButton_5, 
QPushButton#pushButton_7 {
    background-color: #404040;
    color: #e0e0e0;
    min-width: 180px;
}

QPushButton#pushButton_3:hover,
QPushButton#pushButton_6:hover,
QPushButton#pushButton_2:hover, 
QPushButton#pushButton_5:hover, 
QPushButton#pushButton_7:hover {
    background-color: #4a4a4a;
}

QPushButton#pushButton_5 {
    min-width: 200px;
}

QLineEdit {
    border: 2px solid #404040;
    padding: 10px;
    font-size: 14px;
    border-radius: 4px;
    background-color: #2d2d2d;
    color: #e0e0e0;
    min-height: 20px;
}

QLineEdit:focus {
    border: 2px solid #4CAF50;
    background-color: #353535;
}

QDateTimeEdit {
    border: 2px solid #404040;
    padding: 8px;
    border-radius: 4px;
    background-color: #2d2d2d;
    color: #e0e0e0;
    font-size: 14px;
    min-height: 25px;
}

QDateTimeEdit:focus {
    border: 2px solid #4CAF50;
}

QStatusBar {
    background-color: #404040;
    color: #e0e0e0;
    padding: 5px;
    font-size: 12px;
}

QMenuBar {
    background-color: #404040;
    color: #e0e0e0;
    padding: 6px;
    font-size: 14px;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 10px;
}

QMenuBar::item:selected {
    background-color: #4CAF50;
}

QWidget#layoutWidget {
    background-color: transparent;
}

QWidget#centralwidget {
    background-color: #2d2d2d;
}

QFormLayout {
    margin: 5px;
    spacing: 5px;
}

QVBoxLayout {
    margin: 5px;
    spacing: 5px;
}
'''

light_style = '''
QMainWindow {
    background-color: #f5f5f5;
    color: #333333;
}

QWidget {
    background-color: #f5f5f5;
    color: #333333;
}

QTableView {
    background-color: #ffffff;
    color: #333333;
    border: 2px solid #dddddd;
    font-size: 14px;
    gridline-color: #dddddd;
    outline: none;
}

QTableView::item {
    background-color: #ffffff;
    color: #333333;
    padding: 8px;
    border-bottom: 1px solid #eeeeee;
    min-height: 25px;
}

QTableView::item:selected {
    background-color: #4CAF50;
    color: #ffffff;
}

QTableView::item:hover {
    background-color: #f0f0f0;
}

QHeaderView {
    background-color: #e0e0e0;
    color: #333333;
}

QHeaderView::section {
    background-color: #e0e0e0;
    color: #333333;
    padding: 8px;
    border: 1px solid #f5f5f5;
    font-weight: bold;
    font-size: 14px;
    min-height: 30px;
}

QTableCornerButton::section {
    background-color: #e0e0e0;
    border: 1px solid #f5f5f5;
}

QPushButton {
    background-color: #4CAF50;
    color: #ffffff;
    border: none;
    padding: 10px 16px;
    font-size: 14px;
    border-radius: 4px;
    min-height: 20px;
    min-width: 120px;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b40;
}

QPushButton#pushButton_3,
QPushButton#pushButton_6, 
QPushButton#pushButton_2, 
QPushButton#pushButton_5, 
QPushButton#pushButton_7 {
    background-color: #e0e0e0;
    color: #333333;
    min-width: 180px;
}

QPushButton#pushButton_3:hover,
QPushButton#pushButton_6:hover,
QPushButton#pushButton_2:hover, 
QPushButton#pushButton_5:hover, 
QPushButton#pushButton_7:hover {
    background-color: #d6d6d6;
}

QPushButton#pushButton_5 {
    min-width: 200px;
}

QLineEdit {
    border: 2px solid #dddddd;
    padding: 10px;
    font-size: 14px;
    border-radius: 4px;
    background-color: #ffffff;
    color: #333333;
    min-height: 20px;
}

QLineEdit:focus {
    border: 2px solid #4CAF50;
    background-color: #fafafa;
}

QDateTimeEdit {
    border: 2px solid #dddddd;
    padding: 8px;
    border-radius: 4px;
    background-color: #ffffff;
    color: #333333;
    font-size: 14px;
    min-height: 25px;
}

QDateTimeEdit:focus {
    border: 2px solid #4CAF50;
}

QStatusBar {
    background-color: #e0e0e0;
    color: #333333;
    padding: 5px;
    font-size: 12px;
}

QMenuBar {
    background-color: #e0e0e0;
    color: #333333;
    padding: 6px;
    font-size: 14px;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 10px;
}

QMenuBar::item:selected {
    background-color: #4CAF50;
    color: #ffffff;
}

QWidget#layoutWidget {
    background-color: transparent;
}

QWidget#centralwidget {
    background-color: #f5f5f5;
}

QFormLayout {
    margin: 5px;
    spacing: 5px;
}

QVBoxLayout {
    margin: 5px;
    spacing: 5px;
}
'''

tempalte = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>798</width>
    <height>683</height>
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
      <x>1</x>
      <y>421</y>
      <width>791</width>
      <height>221</height>
     </rect>
    </property>
    <layout class="QGridLayout" name="gridLayout">
     <item row="0" column="0">
      <widget class="QPushButton" name="pushButton_4">
       <property name="enabled">
        <bool>true</bool>
       </property>
       <property name="text">
        <string>Создать</string>
       </property>
      </widget>
     </item>
     <item row="0" column="1">
      <widget class="QPushButton" name="pushButton_6">
       <property name="text">
        <string>Удалить категорию</string>
       </property>
      </widget>
     </item>
     <item row="1" column="0">
      <widget class="QLineEdit" name="lineEdit">
       <property name="placeholderText">
        <string>Для создания нового дела напишите название</string>
       </property>
      </widget>
     </item>
     <item row="1" column="1">
      <widget class="QPushButton" name="pushButton_2">
       <property name="text">
        <string>Импортировать задачи</string>
       </property>
      </widget>
     </item>
     <item row="2" column="0">
      <widget class="QPushButton" name="pushButton_3">
       <property name="text">
        <string>Удалить дело</string>
       </property>
      </widget>
     </item>
     <item row="2" column="1">
      <widget class="QPushButton" name="pushButton_5">
       <property name="text">
        <string>сделать тёмную тему</string>
       </property>
      </widget>
     </item>
     <item row="3" column="0">
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
     <item row="3" column="1">
      <widget class="QPushButton" name="pushButton_7">
       <property name="text">
        <string>установить дату и времея напоминания</string>
       </property>
      </widget>
     </item>
     <item row="4" column="0">
      <widget class="QLineEdit" name="lineEdit_2">
       <property name="placeholderText">
        <string>Для создания новой категории напишите здесь название </string>
       </property>
      </widget>
     </item>
     <item row="4" column="1">
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
        self.theme = self.load_theme_from_config()
        self.setup_tray_icon()
        self.load_date_from_config()
        self.apply_theme()
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.set_notify)
        self.check_timer.start(60)

        self.pushButton_4.clicked.connect(self.create_task)
        self.pushButton.clicked.connect(self.new_cattegory)
        self.pushButton_3.clicked.connect(self.delete_task)
        self.pushButton_2.clicked.connect(self.import_base)
        self.pushButton_7.clicked.connect(self.set_notify)
        self.pushButton_6.clicked.connect(self.delete_category)
        self.pushButton_5.clicked.connect(self.change_theme)

        self.dateTimeEdit.dateTimeChanged.connect(self.save_date_to_config)

    def load_theme_from_config(self):
        try:
            with open('config.txt', mode='r', encoding='utf-8') as file:
                content = file.read().strip()
                if 'color_theme = 1' in content:
                    return True
                else:
                    return False
        except FileNotFoundError:
            with open('config.txt', mode='w', encoding='utf-8') as file:
                file.write('color_theme = 0')
            return False

    def save_theme_to_config(self):
        if self.theme:
            theme_value = 1
        else:
            theme_value = 0
        with open('config.txt', mode='w', encoding='utf-8') as file:
            file.write(f'color_theme = {theme_value}')

    def change_theme(self):
        self.theme = not self.theme
        self.apply_theme()
        self.save_theme_to_config()

    def apply_theme(self):
        if self.theme:
            self.setStyleSheet(dark_style)
            self.pushButton_5.setText('Сделать светлую тему')
        else:
            self.setStyleSheet(light_style)
            self.pushButton_5.setText('Сделать тёмную тему')

    def setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))

        tray_menu = QMenu()

        show_action = QAction('Показать', self)
        hide_action = QAction('Скрыть', self)
        quit_action = QAction('Выход', self)

        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.quit_application)

        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activate)
        self.tray_icon.show()

    def on_tray_activate(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            'Smart Task Manager',
            'Приложение продолжает работать в фоне',
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def quit_application(self):
        self.tray_icon.hide()
        QApplication.quit()

    def setup_table(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('tasks.db')

        if not self.db.open():
            raise Db_not_open

        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('tasks_table')
        self.model.select()
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, 'Задача')
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        self.tableView.show()

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks_table (
                tasks NUMERIC UNIQUE NOT NULL
            )
        ''').fetchall()

        self.cur.execute('SELECT COUNT(*) FROM tasks_table')

        row_count = self.cur.fetchone()[0]

        if row_count == 0:
            self.cur.execute('''
                INSERT INTO tasks_table (tasks) 
                VALUES ('Важное дело')
            ''')
        self.save_data()

    def delete_category(self):
        try:
            selected_indexes = self.tableView.selectedIndexes()
            if not selected_indexes:
                self.statusBar().showMessage('Выделите ячейку в колонке для удаления')
                return

            selected_column = selected_indexes[0].column()

            if selected_column == 0:
                self.statusBar().showMessage('Нельзя удалить основную колонку с задачами')
                return

            all_columns = []
            for i in range(self.model.columnCount()):
                all_columns.append(self.model.headerData(i, Qt.Orientation.Horizontal))

            new_columns = [col for i, col in enumerate(all_columns) if i != selected_column]

            columns_str = ', '.join(new_columns)
            self.cur.execute(f'CREATE TABLE temp_table AS SELECT {columns_str} FROM tasks_table')
            self.cur.execute('DROP TABLE tasks_table')
            self.cur.execute('ALTER TABLE temp_table RENAME TO tasks_table')
            self.save_data()

            self.statusBar().showMessage('Категория удалена')

        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e}')

    def delete_task(self):
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
                print(f'Ошибка удаления: {e}')
        self.save_data()

    def new_cattegory(self):
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
        line_text = self.lineEdit.text()
        if line_text != '':
            record = self.model.record()
            record.setValue('tasks', line_text)
            if self.model.insertRecord(-1, record):
                self.lineEdit.clear()
                self.statusBar().showMessage('Успешно добавлено!')
                self.save_data()
            else:
                self.statusBar().showMessage('Ошибка при добавлении задачи')
        else:
            self.statusBar().showMessage('Поле пустое')

    def import_base(self):
        try:
            file_name = 'tasks.db'
            path = QFileDialog.getSaveFileName(self, caption='Сохранить файл',
                                               directory='tasks.db',
                                               filter='All Files')
            shutil.copy(file_name, path[0])
        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e}')

    def save_data(self):

        self.con.commit()
        self.tableView.setModel(None)
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('tasks_table')
        self.model.select()
        self.tableView.setModel(self.model)

    def load_date_from_config(self):
        try:
            with open('config.txt', mode='r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith('reminder_date = '):
                        date_str = line.replace('reminder_date = ', '').strip()
                        date_time = QDateTime.fromString(date_str, 'yyyy-MM-dd HH:mm')
                        if date_time.isValid():
                            self.dateTimeEdit.setDateTime(date_time)
                        else:
                            self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
                        return
        except FileNotFoundError:
            self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

    def save_date_to_config(self):
        try:
            theme_value = 0
            try:
                with open('config.txt', mode='r', encoding='utf-8') as file:
                    lines = file.readlines()
                    for line in lines:
                        if line.startswith('color_theme = '):
                            theme_value = int(line.replace('color_theme = ', '').strip())
            except FileNotFoundError:
                pass

            current_date = self.dateTimeEdit.dateTime().toString('yyyy-MM-dd HH:mm')
            with open('config.txt', mode='w', encoding='utf-8') as file:
                file.write(f'color_theme = {theme_value}\n')
                file.write(f'reminder_date = {current_date}\n')

        except Exception as e:
            print(f'Ошибка: {e}')

    def set_notify(self):
        try:
            current_datetime = QDateTime.currentDateTime()
            reminder_datetime = self.dateTimeEdit.dateTime()
            current_str = current_datetime.toString('dd.MM.yyyy HH:mm')
            reminder_str = reminder_datetime.toString('dd.MM.yyyy HH:mm')

            if current_str == reminder_str:
                notification.notify(
                    title='Напоминание о задаче',
                    message='Вы установили напоминание на это время!',
                    timeout=15,
                    app_name='Smart Task Manager'
                )
                self.statusBar().showMessage('Напоминание сработало!')

                new_time = QDateTime.currentDateTime().addSecs(60)
                self.dateTimeEdit.setDateTime(new_time)
                self.save_date_to_config()

        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimplePlanner()
    window.show()
    sys.exit(app.exec())
