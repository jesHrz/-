from check_window import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
import common


class CHECKFunc(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, main):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.main = main

        self.tableWidget.doubleClicked.connect(self.__delete)

    def init(self):
        self.classes = common.check_classes(self.main.login.sdu)
        size = len(self.classes)
        self.tableWidget.setRowCount(size)
        i = 0
        for cla in self.classes:
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(cla['KCH']))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(cla['KCM']))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(cla['KXH']))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(cla['SJDD']))
            self.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(cla['JSM']))
            self.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(cla['SX']))
            i += 1

    def __delete(self):
        index = self.tableWidget.currentRow()
        current = self.classes[index]
        info = '确定退选课程 %s (%s - %s) 吗?' % (current['KCM'], current['KCH'], current['KXH'])
        button = QtWidgets.QMessageBox.question(self, "确认", self.tr(info),
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                QtWidgets.QMessageBox.Yes)
        if button == QtWidgets.QMessageBox.Yes:
            data = {
                "aoData": "",
                "kchkxh": current['KCH'] + "|" + current['KXH']
            }
            response = self.main.login.sdu.emit("http://bkjwxk.sdu.edu.cn/b/xk/xs/delete", "post", data)
            type = response['result']
            msg = response['msg']
            if type == "error":
                QtWidgets.QMessageBox.critical(self, "错误", self.tr(msg))
            else:
                QtWidgets.QMessageBox.about(self, "成功", self.tr(msg))
                self.tableWidget.removeRow(index)
