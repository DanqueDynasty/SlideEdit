from PyQt4 import QtCore, QtGui
import math

class BoundsDialog(QtGui.QDialog):
    def __init__(self):
        super(BoundsDialog, self).__init__()
        _minLbl = QtGui.QLabel("Min: ", self)
        self._minLE = QtGui.QLineEdit(self);
        _maxLbl = QtGui.QLabel("Max: ", self)
        self._maxLE = QtGui.QLineEdit(self)

        propLayout = QtGui.QGridLayout()
        propLayout.addWidget(_minLbl, 0, 0)
        propLayout.addWidget(self._minLE, 0, 2)
        propLayout.addWidget(_maxLbl, 1, 0)
        propLayout.addWidget(self._maxLE,  1, 2)

        grpBox = QtGui.QGroupBox(self)
        grpBox.setTitle("Properties: ")
        grpBox.setLayout(propLayout)

        _applyBtn = QtGui.QPushButton("Apply", self)
        _cancelBtn = QtGui.QPushButton("Cancel", self)

        btnLayout = QtGui.QHBoxLayout()
        btnLayout.addWidget(_applyBtn)
        btnLayout.addWidget(_cancelBtn)

        centralLayout = QtGui.QVBoxLayout()
        centralLayout.addWidget(grpBox)
        centralLayout.addLayout(btnLayout)
        self.setLayout(centralLayout)

class SlideEdit(QtGui.QLineEdit):
    valueChanged = QtCore.pyqtSignal(object)

    def __init__(self):
        super(SlideEdit, self).__init__()
        self._boundsDiag = BoundsDialog()
        self.setAlignment(QtCore.Qt.AlignCenter)
        self._min = 0.0
        self._max = 10.0
        self._currentValue = 10.0
        self.setText("10")
        self._lockBounds = True
        self._integerStep = True
        self.handle = QtCore.QRect()
        self.progressed = QtCore.QRect()
        self._isDown = False
        self._foregroundColor = QtGui.QColor(83, 125, 148).lighter(120)
        self._foregroundColor.setAlphaF(0.7)
        self.textChanged.connect(self.setCurrentValueStr)

        #Context Menu Actions
        self._resetBoundsAct = QtGui.QAction("Reset Bounds", self)
        self._lockBoundsAct = QtGui.QAction("Lock Bounds", self)
        self._resetMin = QtGui.QAction("Reset Min", self)
        self._resetMax = QtGui.QAction("Reset Max", self)
        self._intStep = QtGui.QAction("Int Step", self)
        self._boundsDiagAct = QtGui.QAction("Edit Bounds", self)


    def setCurrentValue(self, newValue):
        curVal = 0
        if self._integerStep is False:
            curVal = newValue
        else:
            if newValue < 0.5:
                curVal = 0
            else:
                curVal = math.ceil(newValue)

        if self._currentValue > self._max and self._lockBounds is False:
            self._max = newValue
        elif self._currentValue > self._max and self._lockBounds is True:
            curVal = self._max

        self._currentValue = curVal
        self.setText(QtCore.QString.number(self._currentValue))
        self.valueChanged.emit(self._currentValue)

    def setCurrentValueStr(self, value):
        if type(value) is QtCore.QString:
            f = value.toFloat()
            self.setCurrentValue(value.toFloat()[0])

    def mousePressEvent(self, QMouseEvent):
        if (QMouseEvent.button() == 1) and self.handle.contains(QMouseEvent.pos()):
            self._isDown = True

    def mouseReleaseEvent(self, QMouseEvent):
        if self._isDown is True:
            self._isDown = False

    def mouseMoveEvent(self, QMouseEvent):
        #Cursor Stuff
        if self.handle.contains(QMouseEvent.pos()):
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        else:
            self.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        if self._isDown:
            px = QMouseEvent.pos().x()
            print (px / self.width())
            if(px >= 0 and px <= self.width()):
                self.handle.setX(px)
                self._lockBounds = True
                self.setCurrentValue( (px / float(self.width())) * self._max )
                self._lockBounds = False

    def wheelEvent(self, QWheelEvent):
        step = QWheelEvent.delta() / float(80.0)
        curVal = self._currentValue - step
        if self._lockBounds is True:
            if curVal > self._max:
                self.setCurrentValue(self._max)
                return
            elif curVal < self._min:
                self.setCurrentValue(self._min)
                return
            else:
                self.setCurrentValue(curVal)
                return
        self.setCurrentValue(curVal)

    def paintEvent(self, QPaintEvent):
        super(SlideEdit, self).paintEvent(QPaintEvent)
        ratio = self._currentValue / self._max
        pX = ratio * self.geometry().width()
        if(pX <= 12):
            self.handle.setX(self._min)
            self._currentValue = self._min
        else:
            self.handle.setX(pX - 12)

        self.handle.setY(0)
        self.handle.setWidth(12)
        self.handle.setHeight(self.height())

        self.progressed.setX(0)
        self.progressed.setY(0)
        self.progressed.setWidth(self.handle.x())
        self.progressed.setHeight(self.height())

        p = QtGui.QPainter(self)
        p.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        p.drawRect(self.handle)
        p.fillRect(self.handle, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        p.setBrush(QtGui.QBrush(self._foregroundColor))
        p.drawRect(self.progressed)

    def contextMenuEvent(self, QContextMenuEvent):
        menu = QtGui.QMenu(self)
        menu.addAction(self._resetBoundsAct)
        menu.addAction(self._lockBoundsAct)
        menu.addSeparator()
        menu.addAction(self._resetMin)
        menu.addAction(self._resetMax)
        menu.addSeparator()
        menu.addAction(self._boundsDiagAct)
        menu.exec_(QContextMenuEvent.globalPos())
