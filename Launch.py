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
        slideEdit._max = 100
        slideEdit.setCurrentValue(100)
        valuelbl = QtGui.QLabel("Value: ", self)
        self.valueDisp = QtGui.QLabel("&", self)
        layout = QtGui.QGridLayout()
        closeBtn = QtGui.QPushButton("Close", self)
        closeBtn.clicked.connect(self.close)
        layout.addWidget(slideEdit, 0, 0)
        layout.addWidget(valuelbl, 0, 2)
        layout.addWidget(self.valueDisp, 0, 4)
        layout.addWidget(closeBtn, 2, 0)
        centWidget = QtGui.QWidget(self)
        centWidget.setLayout(layout)
        self.setCentralWidget(centWidget)
        slideEdit.valueChanged.connect(self.displayValue)


    def displayValue(self, value):
        self.valueDisp.setText(QtCore.QString.number(value))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())