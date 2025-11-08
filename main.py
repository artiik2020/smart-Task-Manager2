import io
import sys
import sqlite3
import shutil

from PyQt6 import uic
from PyQt6.QtCore import Qt, QDateTime, QTimer
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from plyer import notification


class Db_not_open():
    pass


dark_style = '''
QMainWindow, QWidget {
    background-color: #2d2d2d;
    color: #ffffff;
}

QTableView {
    background-color: #3c3c3c;
    color: #ffffff;
    border: 2px solid #555555;
    font-size: 14px;
    gridline-color: #555555;
}

QTableView::item {
    background-color: #3c3c3c;
    color: #ffffff;
    padding: 8px;
    border-bottom: 1px solid #555555;
}

QTableView::item:selected {
    background-color: #0078d4;
    color: #ffffff;
}

QHeaderView::section {
    background-color: #404040;
    color: #ffffff;
    padding: 8px;
    border: 1px solid #555555;
    font-weight: bold;
}

QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 4px 16px;
    font-size: 11px;
    border-radius: 4px;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b40;
}

#pushButton_3 {
    background-color: #f44336;
}

#pushButton_3:hover {
    background-color: #da190b;
}

#pushButton_6 {
    background-color: #ff9800;
}

#pushButton_6:hover {
    background-color: #e68900;
}

#pushButton_2 {
    background-color: #2196F3;
}

#pushButton_2:hover {
    background-color: #0b7dda;
}

#pushButton_5 {
    background-color: #757575;
}

#pushButton_5:hover {
    background-color: #616161;
}

#pushButton_7 {
    background-color: #9C27B0;
}

#pushButton_7:hover {
    background-color: #7b1fa2;
}

QLineEdit {
    border: 2px solid #555555;
    padding: 4px;
    font-size: 11px;
    border-radius: 4px;
    background-color: #404040;
    color: white;
}

QLineEdit:focus {
    border-color: #4CAF50;
}

QLineEdit::placeholder {
    color: #aaaaaa;
}

QDateTimeEdit {
    border: 2px solid #555555;
    padding: 4px;
    border-radius: 4px;
    background-color: #404040;
    color: white;
}

QStatusBar {
    background-color: #404040;
    color: #cccccc;
}

QMenuBar {
    background-color: #404040;
    color: white;
    padding: 4px;
}'''

light_style = '''
QMainWindow {
    background-color: #f0f0f0;
}

QTableView {
    background-color: white;
    border: 2px solid #cccccc;
    font-size: 11px;
}

QTableView::item {
    padding: 8px;
    border-bottom: 1px solid #eeeeee;
}

QTableView::item:selected {
    background-color: #b3d9ff;
}

QHeaderView::section {
    background-color: #e6e6e6;
    padding: 8px;
    border: 1px solid #cccccc;
    font-weight: bold;
}

QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 4px 11px;
    font-size: 11px;
    border-radius: 2px;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b40;
}

#pushButton_3 {
    background-color: #f44336;
}

#pushButton_3:hover {
    background-color: #da190b;
}

#pushButton_6 {
    background-color: #ff9800;
}

#pushButton_6:hover {
    background-color: #e68900;
}

#pushButton_2 {
    background-color: #2196F3;
}

#pushButton_2:hover {
    background-color: #0b7dda;
}

#pushButton_5 {
    background-color: #757575;
}

#pushButton_5:hover {
    background-color: #616161;
}

#pushButton_7 {
    background-color: #9C27B0;
}

#pushButton_7:hover {
    background-color: #7b1fa2;
}

QLineEdit {
    border: 4px solid #cccccc;
    padding: 4px;
    font-size: 10px;
    border-radius: 8px;
    background-color: white;
}

QLineEdit:focus {
    border-color: #4CAF50;
}

QDateTimeEdit {
    border: 2px solid #cccccc;
    padding: 4px;
    border-radius: 4px;
    background-color: white;
}

QStatusBar {
    background-color: #e6e6e6;
    color: #666666;
}

QMenuBar {
    background-color: #e6e6e6;
    padding: 4px;
}
'''

tempalte = '''<?xml version='1.0' encoding='UTF-8'?>
<ui version='4.0'>
 <class>MainWindow</class>
 <widget class='QMainWindow' name='MainWindow'>
  <property name='geometry'>
   <rect>
    <x>0</x>
    <y>0</y>
    <width>798</width>
    <height>600</height>
   </rect>
  </property>
  <property name='windowTitle'>
   <string>MainWindow</string>
  </property>
  <widget class='QWidget' name='centralwidget'>
   <widget class='QTableView' name='tableView'>
    <property name='geometry'>
     <rect>
      <x>5</x>
      <y>11</y>
      <width>791</width>
      <height>411</height>
     </rect>
    </property>
   </widget>
   <widget class='QWidget' name='layoutWidget'>
    <property name='geometry'>
     <rect>
      <x>0</x>
      <y>420</y>
      <width>401</width>
      <height>164</height>
     </rect>
    </property>
    <layout class='QFormLayout' name='formLayout'>
     <item row='0' column='1'>
      <widget class='QPushButton' name='pushButton_4'>
       <property name='enabled'>
        <bool>true</bool>
       </property>
       <property name='text'>
        <string>Создать</string>
       </property>
      </widget>
     </item>
     <item row='1' column='1'>
      <widget class='QLineEdit' name='lineEdit'>
       <property name='placeholderText'>
        <string>Для создания нового дела напишите название</string>
       </property>
      </widget>
     </item>
     <item row='2' column='1'>
      <widget class='QPushButton' name='pushButton_3'>
       <property name='text'>
        <string>Удалить дело</string>
       </property>
      </widget>
     </item>
     <item row='3' column='1'>
      <widget class='QPushButton' name='pushButton'>
       <property name='maximumSize'>
        <size>
         <width>16777215</width>
         <height>23</height>
        </size>
       </property>
       <property name='text'>
        <string>Новая категория</string>
       </property>
      </widget>
     </item>
     <item row='4' column='1'>
      <widget class='QLineEdit' name='lineEdit_2'>
       <property name='placeholderText'>
        <string>Для создания новой категории напишите здесь название </string>
       </property>
      </widget>
     </item>
    </layout>
   </widget>
   <widget class='QWidget' name='layoutWidget'>
    <property name='geometry'>
     <rect>
      <x>400</x>
      <y>420</y>
      <width>391</width>
      <height>141</height>
     </rect>
    </property>
    <layout class='QVBoxLayout' name='verticalLayout'>
     <item>
      <widget class='QPushButton' name='pushButton_6'>
       <property name='text'>
        <string>Удалить категорию</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class='QPushButton' name='pushButton_2'>
       <property name='text'>
        <string>Импортировать задачи</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class='QPushButton' name='pushButton_5'>
       <property name='text'>
        <string>сделать тёмную тему</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class='QPushButton' name='pushButton_7'>
       <property name='text'>
        <string>установить дату и времея напоминания</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class='QDateTimeEdit' name='dateTimeEdit'/>
     </item>
    </layout>
   </widget>
  </widget>
  <widget class='QStatusBar' name='statusbar'/>
  <widget class='QMenuBar' name='menubar'>
   <property name='geometry'>
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
        self.load_theme()
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.set_notify)
        self.check_timer.start(60000)

        self.pushButton_4.clicked.connect(self.create_task)
        self.pushButton.clicked.connect(self.new_cattegory)
        self.pushButton_3.clicked.connect(self.delete_task)
        self.pushButton_2.clicked.connect(self.import_base)
        self.pushButton_7.clicked.connect(self.set_notify)
        self.pushButton_6.clicked.connect(self.delete_category)

    def setup_table(self):
        '''работает'''
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
        '''Работает(наконец-то)'''
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
        '''работает'''
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
        '''работает'''
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
        '''сохранение данных в таблицу'''
        self.con.commit()
        self.tableView.setModel(None)
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('tasks_table')
        self.model.select()
        self.tableView.setModel(self.model)

    def load_theme(self):
        with open('config.txt', mode='r', encoding='utf8') as file:
            reader = file.readlines()
            print(reader[0][-1])
            if reader[0][-1] == '0':
                self.setStyleSheet(dark_style)
                self.pushButton_5.setText('Сделать светлую тему')
                with open('config.txt', mode='w', encoding='utf8') as file1:
                    writer = file1.write('color_theme = 1')
                self.statusBar().showMessage('Перезапустите приложение')
            elif reader[0][-1] == '1':
                self.setStyleSheet(light_style)
                self.pushButton_5.setText('Сделать тёмную тему')
                with open('config.txt', mode='w', encoding='utf8') as file1:
                    writer = file1.write('color_theme = 0')
                self.statusBar().showMessage('Перезапустите приложение')

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

        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimplePlanner()
    window.show()
    sys.exit(app.exec())
