# -*- coding: utf-8 -*-


from main_window import Ui_MainWindow
from PyQt5 import QtWidgets
from login_window_func import LOGINFunc
from check_window_func import CHECKFunc
import common
import webbrowser
import json
import threading
import win10toast

"""     主界面方法控制     """


class MAINWindowFunc(QtWidgets.QMainWindow, Ui_MainWindow):
    __lock = threading.RLock()

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.started = False

        self.login = LOGINFunc(self)
        self.check = CHECKFunc(self)

        #   设置按钮信息槽
        self.button_search.clicked.connect(self.__threading_search)  # 使用多线程 避免出现未响应情况
        self.button_start.clicked.connect(self.__start_monitoring)
        self.button_stop.clicked.connect(self.__stop_monitoring)

        #   设置菜单栏信息槽
        self.action_login.triggered.connect(self.__start_login)
        self.action_check.triggered.connect(self.__check)
        self.action_exit.triggered.connect(self.close)
        self.action_update.triggered.connect(self.__update)
        self.action_about.triggered.connect(self.__about)

        self.table_info.doubleClicked.connect(self.__select)

    #   查询课程信息并显示在table_info中
    def __search(self, monitoring):

        try:
            self.line_time.setEnabled(not self.started)
            self.button_start.setEnabled(not self.started)
            self.statusbar.showMessage("查询中")

            kch = self.line_kch.text()
            jsh = self.line_jsm.text()
            kkxsh = self.line_xy.text()
            xq = self.comboBox_xq.currentText()
            jc = self.comboBox_jc.currentText()
            dd = self.comboBox_dd.currentText()
            self.classes = common.search_classes(self.login.sdu, kch, jsh, xq, jc, kkxsh, dd)

            size = len(self.classes)
            self.table_info.setRowCount(size)

            i = 0
            for cla in self.classes:
                # monitoring==True 表示正在监视   发现有课余量后会发系统通知
                if monitoring:
                    toaster = win10toast.ToastNotifier()
                    if (cla['kyl'] > 0):
                        last_kcm = cla['KCM']
                        last_jsm = cla['JSM']
                        if last_kcm is None:
                            last_kcm = ''
                        if last_jsm is None:
                            last_jsm = ''
                        toaster.show_toast("发现剩余课余量", last_kcm + " " + last_jsm, icon_path='icon/favicon.ico',
                                           duration=5)
                        self.__stop_monitoring()

                self.table_info.setItem(i, 0, QtWidgets.QTableWidgetItem(cla['KCH']))
                self.table_info.setItem(i, 1, QtWidgets.QTableWidgetItem(cla['KXH']))
                self.table_info.setItem(i, 2, QtWidgets.QTableWidgetItem(cla['KCM']))
                self.table_info.setItem(i, 3, QtWidgets.QTableWidgetItem(str(cla['XF'])))
                self.table_info.setItem(i, 4, QtWidgets.QTableWidgetItem(cla['JSM']))
                self.table_info.setItem(i, 5, QtWidgets.QTableWidgetItem(str(cla['kyl'])))
                self.table_info.setItem(i, 6, QtWidgets.QTableWidgetItem(cla['SJDD']))

                i += 1

        finally:
            self.statusbar.showMessage("查询完毕")
            self.button_start.setEnabled(not self.started)
            self.line_time.setEnabled(not self.started)

    #   调出登陆界面
    def __start_login(self):
        self.login.show()
        self.login.line_username.setFocus()

    def __check(self):
        self.check.show()
        self.check.init()

    #   启动监视    以毫秒为单位
    def __start_monitoring(self):
        time = self.line_time.text()
        if time == '':
            time = '2000'
        try:
            time = int(time)
        except TypeError:
            QtWidgets.QMessageBox.information(self, "提示", "请输入有效数字")
            self.line_time.clear()
        else:
            if 0 > time:
                QtWidgets.QMessageBox.information(self, "提示", "请输入非零数字")
                self.line_time.clear()
            else:
                self.timer.timeout.connect(self.__threading_search)
                self.timer.start(time)
                self.started = True
                self.setEnable(False)
                self.button_stop.setEnabled(True)

    #   结束监视
    def __stop_monitoring(self):
        self.timer.stop()
        self.setEnable(True)
        self.button_stop.setEnabled(False)
        self.started = False

    def __select(self):
        index = self.table_info.currentRow()
        current = self.classes[index]
        info = '确定选择课程 %s (%s - %s) 吗?' % (current['KCM'], current['KCH'], current['KXH'])
        button = QtWidgets.QMessageBox.question(self, "确认", self.tr(info),
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                QtWidgets.QMessageBox.Yes)
        if button == QtWidgets.QMessageBox.Yes:
            response = self.login.sdu.emit(
                "http://bkjwxk.sdu.edu.cn/b/xk/xs/add/%s/%s" % (current['KCH'], current['KXH']), "get")
            ret = json.loads(response)
            type = ret['result']
            msg = ret['msg']
            if type == "error":
                QtWidgets.QMessageBox.critical(self, "错误", self.tr(msg))
            else:
                QtWidgets.QMessageBox.about(self, "成功", self.tr(msg))

    def __threading_search(self):
        monitor_type = True
        if self.sender() == self.button_search:
            monitor_type = False
        t = threading.Thread(target=self.__search, args=(monitor_type,))
        t.setDaemon(True)
        t.start()

    def __update(self):
        webbrowser.open("https://github.com/jesHrz/SDU-classAssistant", new=2)

    def __about(self):
        QtWidgets.QMessageBox.information(self, "滑稽", "欢迎与作者进行哲♂学交流")
