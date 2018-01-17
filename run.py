from main_window_func import MAINWindowFunc
from PyQt5 import QtWidgets
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MAINWindowFunc()
    main_window.show()
    sys.exit(app.exec_())
