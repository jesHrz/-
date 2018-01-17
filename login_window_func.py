from PyQt5 import QtWidgets, QtCore
from login_window import Ui_MainWindow
from sduLogin import SDULogin


class LOGINFunc(QtWidgets.QMainWindow, Ui_MainWindow):
    sdu = None

    def __init__(self, main):
        super(LOGINFunc, self).__init__()
        self.setupUi(self)

        self.main = main
        self.button_login.clicked.connect(self.login)
        self.line_username.returnPressed.connect(self.Focus)
        self.line_pwd.returnPressed.connect(self.login)

    def login(self):
        self.username = self.line_username.text()
        self.pwd = self.line_pwd.text()
        if self.username == "" or self.pwd == "":
            QtWidgets.QMessageBox.information(self, "提示", "学号和密码不能为空")
        else:
            self.sdu = SDULogin(self.username, self.pwd)
            if self.sdu.login("http://bkjwxk.sdu.edu.cn/b/ajaxLogin"):
                QtWidgets.QMessageBox.information(self, "提示", "登录成功")
                self.main.setEnable(True)
                self.main.button_stop.setEnabled(False)
                self.main.statusbar.showMessage(self.username + "  已登录")
                self.close()
            else:
                QtWidgets.QMessageBox.information(self, "提示", "登录失败")
                self.main.setEnable(False)
    def Focus(self):
        self.line_pwd.setFocus()