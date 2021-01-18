import sys
from PyQt5.QtWidgets import *
from auto_main import *


def print_hi(name):
    print(f'Hi, {name}')  # 중단점을 전환하려면 Ctrl+F8 을(를) 누릅니다.


class AutoWindowClass(QMainWindow, Ui_autoMainForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.okBtn.clicked.connect(self.ok_button_event)

    def ok_button_event(self):
        self.okTxtLabel.setText(self.charTxtEdit.toPlainText())


if __name__ == '__main__':
    print_hi('Start Python')

    app = QApplication(sys.argv)
    autoStockWindow = AutoWindowClass()
    autoStockWindow.show()
    sys.exit(app.exec_())
