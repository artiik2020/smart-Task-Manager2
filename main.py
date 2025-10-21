import sys
from PyQt6.QtWidgets import QMainWindow, QApplication


class AntiPlagiarism(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AntiPlagiarism()
    window.show()
    sys.exit(app.exec())
