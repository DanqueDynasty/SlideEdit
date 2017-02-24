from PyQt4 import QtGui, QtCore
import sys

import Util.SlideEdit

from Util.SlideEdit import SlideEdit


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("SlideEdit")
        self.setupUI()

    def setupUI(self):
        slideEdit = SlideEdit()
        layout = QtGui.QGridLayout()
        closeBtn = QtGui.QPushButton("Close", self)
        layout.addWidget(slideEdit, 0, 0)
        layout.addWidget(closeBtn, 2, 0)
        centWidget = QtGui.QWidget(self)
        centWidget.setLayout(layout)
        self.setCentralWidget(centWidget)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())