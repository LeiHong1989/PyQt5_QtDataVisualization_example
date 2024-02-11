import math
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QVector3D, QImage, QLinearGradient
from PyQt5.QtDataVisualization import (Q3DSurface, QSurface3DSeries, QSurfaceDataProxy, QSurfaceDataItem,
                                       QAbstract3DSeries, QValue3DAxis, QAbstract3DGraph, Q3DCamera,
                                       Q3DTheme, QHeightMapSurfaceDataProxy)

sampleCountX = 50
sampleCountZ = 50
heightMapGridStepX = 6
heightMapGridStepZ = 6
sampleMin = -8.0
sampleMax = 8.0


class SurfaceGraph(QObject):
    def __init__(self, surface):
        super(SurfaceGraph, self).__init__()

        self.graph = surface

        self.graph.setAxisX(QValue3DAxis())
        self.graph.setAxisY(QValue3DAxis())
        self.graph.setAxisZ(QValue3DAxis())

        self.sqrtSinProxy = QSurfaceDataProxy()
        self.sqrtSinSeries = QSurface3DSeries(self.sqrtSinProxy)
        self.fillSqrtSinProxy()

        heightMapImage = QImage(':/maps/mountain')
        self.heightMapProxy = QHeightMapSurfaceDataProxy(heightMapImage)
        self.heightMapSeries = QSurface3DSeries(self.heightMapProxy)
        self.heightMapSeries.setItemLabelFormat('(@xLabel, @zLabel): @yLabel')
        self.heightMapProxy.setValueRanges(34.0, 40.0, 18.0, 24.0)

        self.heightMapWidth = heightMapImage.width()
        self.heightMapHeight = heightMapImage.height()

    def toggleModeNone(self):
        self.graph.setSelectionMode(QAbstract3DGraph.SelectionNone)

    def toggleModeItem(self):
        self.graph.setSelectionMode(QAbstract3DGraph.SelectionItem)

    def toggleModeSliceRow(self):
        self.graph.setSelectionMode(QAbstract3DGraph.SelectionItemAndRow | QAbstract3DGraph.SelectionSlice)

    def toggleModeSliceColumn(self):
        self.graph.setSelectionMode(QAbstract3DGraph.SelectionItemAndColumn | QAbstract3DGraph.SelectionSlice)

    def setAxisMinSliderX(self, slider):
        self.axisMinSliderX = slider

    def setAxisMaxSliderX(self, slider):
        self.axisMaxSliderX = slider

    def setAxisMinSliderZ(self, slider):
        self.axisMinSliderZ = slider

    def setAxisMaxSliderZ(self, slider):
        self.axisMaxSliderZ = slider

    def fillSqrtSinProxy(self):
        stepX = (sampleMax - sampleMin) / float(sampleCountX - 1)
        stepZ = (sampleMax - sampleMin) / float(sampleCountZ - 1)

        dataArray = []
        index = 0
        for i in range(sampleCountZ):
            z = min(sampleMax, i * stepZ + sampleMin)
            x_arr = []
            for j in range(sampleCountX):
                x = min(sampleMax, j * stepX + sampleMin)
                R = math.sqrt(z * z + x * x) + 0.01
                y = (math.sin(R) / R + 0.24) * 1.61
                x_arr.append(QSurfaceDataItem(QVector3D(x, y, z)))
            dataArray.append(x_arr)

        self.sqrtSinProxy.resetArray(dataArray)

    def enableSqrtSinModel(self, enable):
        if not enable:
            return

        self.sqrtSinSeries.setDrawMode(QSurface3DSeries.DrawSurfaceAndWireframe)
        self.sqrtSinSeries.setFlatShadingEnabled(True)

        self.graph.axisX().setLabelFormat('%.2f')
        self.graph.axisZ().setLabelFormat('%.2f')
        self.graph.axisX().setRange(sampleMin, sampleMax)
        self.graph.axisY().setRange(0.0, 2.0)
        self.graph.axisZ().setRange(sampleMin, sampleMax)
        self.graph.axisX().setLabelAutoRotation(30)
        self.graph.axisY().setLabelAutoRotation(90)
        self.graph.axisZ().setLabelAutoRotation(30)

        self.graph.removeSeries(self.heightMapSeries)
        self.graph.addSeries(self.sqrtSinSeries)

        # 为Sqrt&Sin 重新设置滑动条范围
        self.rangeMinX = sampleMin
        self.rangeMinZ = sampleMin
        self.stepX = (sampleMax - sampleMin) / float(sampleCountX - 1)
        self.stepZ = (sampleMax - sampleMin) / float(sampleCountZ - 1)
        self.axisMinSliderX.setMaximum(sampleCountX - 2)
        self.axisMinSliderX.setValue(0)
        self.axisMaxSliderX.setMaximum(sampleCountX - 1)
        self.axisMaxSliderX.setValue(sampleCountX - 1)
        self.axisMinSliderZ.setMaximum(sampleCountZ - 2)
        self.axisMinSliderZ.setValue(0)
        self.axisMaxSliderZ.setMaximum(sampleCountZ - 1)
        self.axisMaxSliderZ.setValue(sampleCountZ - 1)

    def enableHeightMapModel(self, enable):
        if not enable:
            return

        self.heightMapSeries.setDrawMode(QSurface3DSeries.DrawSurface)
        self.heightMapSeries.setFlatShadingEnabled(False)

        self.graph.axisX().setLabelFormat('%.1f N')
        self.graph.axisZ().setLabelFormat('%.1f E')
        self.graph.axisX().setRange(34.0, 40.0)
        self.graph.axisY().setAutoAdjustRange(True)
        self.graph.axisZ().setRange(18.0, 24.0)

        self.graph.axisX().setTitle('纬度')
        self.graph.axisY().setTitle('高度')
        self.graph.axisZ().setTitle('经度')

        self.graph.removeSeries(self.sqrtSinSeries)
        self.graph.addSeries(self.heightMapSeries)

        # 重新设置滚动条的范围
        mapGridCountX = self.heightMapWidth / heightMapGridStepX
        mapGridCountZ = self.heightMapHeight / heightMapGridStepZ
        self.rangeMinX = 34.0
        self.rangeMinZ = 18.0
        self.stepX = 6.0 / float(mapGridCountX - 1)
        self.stepZ = 6.0 / float(mapGridCountZ - 1)
        self.axisMinSliderX.setMaximum(mapGridCountX - 2)
        self.axisMinSliderX.setValue(0)
        self.axisMaxSliderX.setMaximum(mapGridCountX - 1)
        self.axisMaxSliderX.setValue(mapGridCountX - 1)
        self.axisMinSliderZ.setMaximum(mapGridCountZ - 2)
        self.axisMinSliderZ.setValue(0)
        self.axisMaxSliderZ.setMaximum(mapGridCountZ - 1)
        self.axisMaxSliderZ.setValue(mapGridCountZ - 1)

    def adjustXMin(self, minVal):
        minX = self.stepX * minVal + self.rangeMinX

        maxVal = self.axisMaxSliderX.value()
        if minVal >= maxVal:
            maxVal = minVal + 1
            self.axisMaxSliderX.setValue(maxVal)
        maxX = self.stepX * maxVal + self.rangeMinX

        self.setAxisXRange(minX, maxX)

    def adjustXMax(self, maxVal):
        maxX = self.stepX * maxVal + self.rangeMinX

        minVal = self.axisMinSliderX.value()
        if maxVal <= minVal:
            minVal = maxVal - 1
            self.axisMinSliderX.setValue(minVal)
        minX = self.stepX * minVal + self.rangeMinX

        self.setAxisXRange(minX, maxX)

    def adjustZMin(self, minVal):
        minZ = self.stepZ * minVal + self.rangeMinZ

        maxVal = self.axisMaxSliderZ.value()
        if minVal >= maxVal:
            maxVal = minVal + 1
            self.axisMaxSliderZ.setValue(maxVal)
        maxZ = self.stepZ * maxVal + self.rangeMinZ

        self.setAxisZRange(minZ, maxZ)

    def adjustZMax(self, maxVal):
        maxZ = self.stepZ * maxVal + self.rangeMinZ

        minVal = self.axisMinSliderZ.value()
        if maxVal <= minVal:
            minVal = maxVal - 1
            self.axisMinSliderZ.setValue(minVal)
        minZ = self.stepZ * minVal + self.rangeMinZ

        self.setAxisZRange(minZ, maxZ)

    def setAxisXRange(self, minVal, maxVal):
        self.graph.axisX().setRange(minVal, maxVal)

    def setAxisZRange(self, minVal, maxVal):
        self.graph.axisZ().setRange(minVal, maxVal)

    def changeTheme(self, theme):
        self.graph.activeTheme().setType(theme)

    def setBlackToYellowGradient(self):
        gr = QLinearGradient()
        gr.setColorAt(0.0, Qt.black)
        gr.setColorAt(0.33, Qt.blue)
        gr.setColorAt(0.67, Qt.red)
        gr.setColorAt(1.0, Qt.yellow)

        self.graph.seriesList()[0].setBaseGradient(gr)
        self.graph.seriesList()[0].setColorStyle(Q3DTheme.ColorStyleRangeGradient)

    def setGreenToRedGradient(self):
        gr = QLinearGradient()
        gr.setColorAt(0.0, Qt.darkGreen)
        gr.setColorAt(0.5, Qt.yellow)
        gr.setColorAt(0.8, Qt.red)
        gr.setColorAt(1.0, Qt.darkRed)

        self.graph.seriesList()[0].setBaseGradient(gr)
        self.graph.seriesList()[0].setColorStyle(Q3DTheme.ColorStyleRangeGradient)
