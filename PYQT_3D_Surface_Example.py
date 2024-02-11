"""
CSDN Link #1:
https://blog.csdn.net/seniorwizard/article/details/130670261

CSDN Link #2:
https://blog.csdn.net/seniorwizard/article/details/130662925

CSDN Link #3:
https://blog.csdn.net/seniorwizard/article/details/130662823
"""





import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QLinearGradient, QPixmap, QPainter, QBrush, QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QSizePolicy,
                             QHBoxLayout, QVBoxLayout, QComboBox, QPushButton,
                             QCheckBox, QSlider, QGroupBox, QLabel, QRadioButton)
from PyQt5.QtDataVisualization import (Q3DSurface, QAbstract3DSeries, QAbstract3DGraph)

from surfacegraph import SurfaceGraph
# import surface_rc


class DemoWidget(QWidget):
    def __init__(self, parent=None):
        super(DemoWidget, self).__init__(parent)

        # 设置窗口标题
        self.setWindowTitle('实战 Qt for Python: 三维表面图演示')
        # 设置窗口大小
        self.resize(640, 480)

        self.initUi()

    def initUi(self):
        widgetgraph = Q3DSurface()
        container = QWidget.createWindowContainer(widgetgraph)
        if not widgetgraph.hasContext():
            msgBox = QMessageBox()
            msgBox.setText('不能初始化OpenGL上下文')
            msgBox.exec()
            return;
        screenSize = widgetgraph.screen().size()
        container.setMinimumSize(QSize(int(screenSize.width() / 2.0), int(screenSize.height() / 1.5)))
        container.setMaximumSize(screenSize)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        container.setFocusPolicy(Qt.StrongFocus)
        hLayout = QHBoxLayout()
        vLayout = QVBoxLayout()
        hLayout.addWidget(container, 1)  # 左边绘图部分
        hLayout.addLayout(vLayout)  # 右边控制部分
        vLayout.setAlignment(Qt.AlignTop)
        modelGroupBox = QGroupBox('模型')
        sqrtSinModelRB = QRadioButton(self)
        sqrtSinModelRB.setText('Sqrt && Sin')
        sqrtSinModelRB.setChecked(False)
        heightMapModelRB = QRadioButton(self)
        heightMapModelRB.setText('高度地图')
        heightMapModelRB.setChecked(False)
        modelVBox = QVBoxLayout()
        modelVBox.addWidget(sqrtSinModelRB)
        modelVBox.addWidget(heightMapModelRB)
        modelGroupBox.setLayout(modelVBox)
        selectionGroupBox = QGroupBox('选择模式')
        modeNoneRB = QRadioButton(self)
        modeNoneRB.setText('无选择')
        modeNoneRB.setChecked(False)
        modeItemRB = QRadioButton(self)
        modeItemRB.setText('条目')
        modeItemRB.setChecked(False)
        modeSliceRowRB = QRadioButton(self)
        modeSliceRowRB.setText('Row Slice')
        modeSliceRowRB.setChecked(False)
        modeSliceColumnRB = QRadioButton(self)
        modeSliceColumnRB.setText('Column Slice')
        modeSliceColumnRB.setChecked(False)
        selectionVBox = QVBoxLayout()
        selectionVBox.addWidget(modeNoneRB)
        selectionVBox.addWidget(modeItemRB)
        selectionVBox.addWidget(modeSliceRowRB)
        selectionVBox.addWidget(modeSliceColumnRB)
        selectionGroupBox.setLayout(selectionVBox)
        axisMinSliderX = QSlider(Qt.Horizontal, self)
        axisMinSliderX.setMinimum(0)
        axisMinSliderX.setTickInterval(1)
        axisMinSliderX.setEnabled(True)
        axisMaxSliderX = QSlider(Qt.Horizontal, self)
        axisMaxSliderX.setMinimum(1)
        axisMaxSliderX.setTickInterval(1)
        axisMaxSliderX.setEnabled(True)
        axisMinSliderZ = QSlider(Qt.Horizontal, self)
        axisMinSliderZ.setMinimum(0)
        axisMinSliderZ.setTickInterval(1)
        axisMinSliderZ.setEnabled(True)
        axisMaxSliderZ = QSlider(Qt.Horizontal, self)
        axisMaxSliderZ.setMinimum(1)
        axisMaxSliderZ.setTickInterval(1)
        axisMaxSliderZ.setEnabled(True)
        # 图表主题控制
        themeList = QComboBox(self)
        themeList.addItem('Qt')
        themeList.addItem('Primary Colors')
        themeList.addItem('Digia')
        themeList.addItem('Stone Moss')
        themeList.addItem('Army Blue')
        themeList.addItem('Retro')
        themeList.addItem('Ebony')
        themeList.addItem('Isabelle')
        themeList.setCurrentIndex(6)
        colorGroupBox = QGroupBox('自定义梯度')
        grBtoY = QLinearGradient(0, 0, 1, 100)
        grBtoY.setColorAt(1.0, Qt.black)
        grBtoY.setColorAt(0.67, Qt.blue)
        grBtoY.setColorAt(0.33, Qt.red)
        grBtoY.setColorAt(0.0, Qt.yellow)
        pm = QPixmap(24, 100)
        pmp = QPainter(pm)
        pmp.setBrush(QBrush(grBtoY))
        pmp.setPen(Qt.NoPen)
        pmp.drawRect(0, 0, 24, 100)
        gradientBtoYPB = QPushButton(self)
        gradientBtoYPB.setIcon(QIcon(pm))
        gradientBtoYPB.setIconSize(QSize(24, 100))
        grGtoR = QLinearGradient(0, 0, 1, 100)
        grGtoR.setColorAt(1.0, Qt.darkGreen)
        grGtoR.setColorAt(0.67, Qt.yellow)
        grGtoR.setColorAt(0.33, Qt.red)
        grGtoR.setColorAt(0.0, Qt.darkRed)
        pmp.setBrush(QBrush(grGtoR))
        pmp.setPen(Qt.NoPen)
        pmp.drawRect(0, 0, 24, 100)
        gradientGtoRPB = QPushButton(self)
        gradientGtoRPB.setIcon(QIcon(pm))
        gradientGtoRPB.setIconSize(QSize(24, 100))
        # 必须控制先后释放顺序
        del pmp
        del pm
        colorHBox = QHBoxLayout()
        colorHBox.addWidget(gradientBtoYPB)
        colorHBox.addWidget(gradientGtoRPB)
        colorGroupBox.setLayout(colorHBox)

        vLayout.addWidget(modelGroupBox)
        vLayout.addWidget(selectionGroupBox)
        vLayout.addWidget(QLabel('列范围'))
        vLayout.addWidget(axisMinSliderX)
        vLayout.addWidget(axisMaxSliderX)
        vLayout.addWidget(QLabel('行范围'))
        vLayout.addWidget(axisMinSliderZ)
        vLayout.addWidget(axisMaxSliderZ)
        vLayout.addWidget(QLabel('主题'))
        vLayout.addWidget(themeList)
        vLayout.addWidget(colorGroupBox)
        self.modifier = SurfaceGraph(widgetgraph)
        heightMapModelRB.toggled.connect(self.modifier.enableHeightMapModel)
        sqrtSinModelRB.toggled.connect(self.modifier.enableSqrtSinModel)
        modeNoneRB.toggled.connect(self.modifier.toggleModeNone)
        modeItemRB.toggled.connect(self.modifier.toggleModeItem)
        modeSliceRowRB.toggled.connect(self.modifier.toggleModeSliceRow)
        modeSliceColumnRB.toggled.connect(self.modifier.toggleModeSliceColumn)

        axisMinSliderX.valueChanged.connect(self.modifier.adjustXMin)
        axisMaxSliderX.valueChanged.connect(self.modifier.adjustXMax)
        axisMinSliderZ.valueChanged.connect(self.modifier.adjustZMin)
        axisMaxSliderZ.valueChanged.connect(self.modifier.adjustZMax)
        themeList.currentIndexChanged.connect(self.modifier.changeTheme)
        gradientBtoYPB.pressed.connect(self.modifier.setBlackToYellowGradient)
        gradientGtoRPB.pressed.connect(self.modifier.setGreenToRedGradient)
        self.modifier.setAxisMinSliderX(axisMinSliderX)
        self.modifier.setAxisMaxSliderX(axisMaxSliderX)
        self.modifier.setAxisMinSliderZ(axisMinSliderZ)
        self.modifier.setAxisMaxSliderZ(axisMaxSliderZ)
        sqrtSinModelRB.setChecked(True)
        modeItemRB.setChecked(True)
        themeList.setCurrentIndex(2)
        self.setLayout(hLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DemoWidget()
    window.show()
    sys.exit(app.exec())
