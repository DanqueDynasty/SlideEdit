from PyQt4 import QtCore, QtGui
import math

class BoundsDialog(QtGui.QDialog):
    def __init__(self):
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
    valueChanged = QtCore.pyqtSignal()

    def __init__(self):
        super(SlideEdit, self).__init__()
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

    def setCurrentValue(self, newValue):
        if self._integerStep is False:
            self._currentValue = newValue
        else:
            if newValue < 0.5:
                self._currentValue = 0
            else:
                self._currentValue = math.ceil(newValue)

        if self._currentValue > self._max and self._lockBounds is False:
            self._max = newValue
        self._currentValue = newValue
        self.setText(QtCore.QString.number(self._currentValue))

    def mousePressEvent(self, QMouseEvent):
        print(QMouseEvent.button());
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
            if(px >= 0 and px <= self.width()):
                self.handle.setX(px)
                self._lockBounds = True
                self.setCurrentValue( (px / self.width()) * self._max )
                self._lockBounds = False

    def wheelEvent(self, QWheelEvent):
        step = QWheelEvent.delta() / 50.0
        curVal = self._currentValue - step
        if self._lockBounds is True:
            if curVal > self._max:
                self.setCurrentValue(self._max)
            elif curVal < self._min:
                self.setCurrentValue(self._min)
            else:
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


