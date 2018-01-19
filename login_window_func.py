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
        self.line_username.returnPressed.connect(self.focus)
        self.line_pwd.returnPressed.connect(self.login)

    def login(self):
        username = self.line_username.text()
        pwd = self.line_pwd.text()
        if username == "" or pwd == "":
            QtWidgets.QMessageBox.information(self, "提示", "学号和密码不能为空")
        else:
            self.sdu = SDULogin(username, pwd)
            result_status, result_info = self.sdu.login("http://bkjwxk.sdu.edu.cn/b/ajaxLogin")
            if result_status:
                self.main.setEnable(True)
                self.main.button_stop.setEnabled(False)
                self.main.statusbar.showMessage(username + "  已登录")
                self.close()
            else:
                QtWidgets.QMessageBox.information(self, "提示", result_info.replace("\"", ''))
                self.main.setEnable(False)

    def focus(self):
        self.line_pwd.setFocus()
