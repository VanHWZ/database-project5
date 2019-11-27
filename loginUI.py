import sys
import dataAccess
import OrganizerUI
import CompetitorUI

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QLineEdit, QLabel, \
    QComboBox, QDialog


class Login(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(800, 400, 300, 220)
        self.setWindowTitle('Login')

        loginButton = QPushButton("Login")
        closeButton = QPushButton("Close")

        loginButton.clicked.connect(self.login)
        closeButton.clicked.connect(QCoreApplication.instance().quit)

        label1 = QLabel("ID:")
        self.lineEdit1 = QLineEdit()
        label2 = QLabel("PW:")
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setEchoMode(QLineEdit.Password)

        self.comboBox = QComboBox()
        self.comboBox.addItem("Competitor")
        self.comboBox.addItem("Organizer")

        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Identity:"))
        hbox1.addWidget(self.comboBox)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(label1)
        hbox2.addWidget(self.lineEdit1)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(label2)
        hbox3.addWidget(self.lineEdit2)

        hbox4 = QHBoxLayout()
        hbox4.addStretch(1)
        hbox4.addWidget(loginButton)
        hbox4.addWidget(closeButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addStretch(1)
        vbox.addLayout(hbox4)

        self.setLayout(vbox)

        # 显示窗口
        self.show()

    def login(self):
        identity = self.comboBox.currentText()
        id = self.lineEdit1.text()
        password = self.lineEdit2.text()


        if dataAccess.login_check(identity, id, password):
            dialog = QDialog()
            dialog.resize(200, 100)
            dialog.setWindowTitle("Dialog")

            label = QLabel("Login successfully!")
            button = QPushButton("confirm")
            button.clicked.connect(dialog.close)

            vbox = QVBoxLayout()
            vbox.addWidget(label)
            vbox.addWidget(button)

            dialog.setLayout(vbox)
            dialog.setWindowModality(Qt.ApplicationModal)
            dialog.exec_()
        else:
            dialog = QDialog()
            dialog.resize(200, 100)
            dialog.setWindowTitle("Dialog")

            label = QLabel("ID or password error!")
            button = QPushButton("confirm")
            button.clicked.connect(dialog.close)

            vbox = QVBoxLayout()
            vbox.addWidget(label)
            vbox.addWidget(button)

            dialog.setLayout(vbox)
            dialog.setWindowModality(Qt.ApplicationModal)
            dialog.exec_()

            self.lineEdit1.clear()
            self.lineEdit2.clear()

        if identity == "Competitor":
            self.close()
            competitor.setWCAid(id)
            competitor.show()
        elif identity == "Organizer":
            self.close()
            organizer.show()



if __name__ == '__main__':
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    login = Login()
    organizer = OrganizerUI.Organizer()
    competitor = CompetitorUI.Competitor("1")
    sys.exit(app.exec_())