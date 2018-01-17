# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(440, 165)
        MainWindow.setMinimumSize(QtCore.QSize(440, 165))
        MainWindow.setMaximumSize(QtCore.QSize(440, 165))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_pwd = QtWidgets.QLabel(self.centralwidget)
        self.label_pwd.setGeometry(QtCore.QRect(60, 65, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(10)
        self.label_pwd.setFont(font)
        self.label_pwd.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_pwd.setObjectName("label_pwd")
        self.label_username = QtWidgets.QLabel(self.centralwidget)
        self.label_username.setGeometry(QtCore.QRect(100, 20, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(10)
        self.label_username.setFont(font)
        self.label_username.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_username.setObjectName("label_username")
        self.button_login = QtWidgets.QPushButton(self.centralwidget)
        self.button_login.setGeometry(QtCore.QRect(260, 110, 112, 34))
        self.button_login.setObjectName("button_login")
        self.line_username = QtWidgets.QLineEdit(self.centralwidget)
        self.line_username.setGeometry(QtCore.QRect(150, 20, 221, 31))
        self.line_username.setObjectName("line_username")
        self.line_pwd = QtWidgets.QLineEdit(self.centralwidget)
        self.line_pwd.setGeometry(QtCore.QRect(150, 60, 221, 31))
        self.line_pwd.setObjectName("line_pwd")
        self.line_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "用户登录"))
        self.label_pwd.setText(_translate("MainWindow", "选课密码"))
        self.label_username.setText(_translate("MainWindow", "学号"))
        self.button_login.setText(_translate("MainWindow", "用户登录"))
