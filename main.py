#!/usr/bin/env python3
import sys
import os
import typing
from typing import Dict, Optional
from PySide2.QtCore import QAbstractListModel, QModelIndex, QObject, QStringListModel, Slot
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QGuiApplication, QIcon
import PySide2.QtQml
from PySide2.QtQuick import QQuickView
from acpi_call import isRapidCharge, isBatteryConservation, getPerfMode, setPerfMode, Mode, setBatteryConservation, setRapidCharge
import icon_rc

opKeys = ["battery conservation mode", "rapid charge"]


def getStatus(name):
    print(f"name: {name}")
    if name == opKeys[0]:
        return isBatteryConservation()
    if name == opKeys[1]:
        return isRapidCharge()


def mapper(k):
    d = dict()
    d['text'] = k
    d['checked'] = getStatus(k)
    return d


class SwitchListModel(QAbstractListModel):
    def __init__(self) -> None:
        super().__init__()
        self.opKeys = list(map(mapper, opKeys))

    def flags(self) -> PySide2.QtCore.Qt.ItemFlags:
        return PySide2.QtCore.Qt.ItemIsEditable

    def rowCount(self, index: QModelIndex) -> int:
        return len(self.opKeys[index.row()])

    def data(self, index: QModelIndex, role: int = 0) -> Dict:
        return self.opKeys[index.row()]

    def setData(self, index: QModelIndex, value: typing.Any, role: int = 0) -> bool:
        self.opKeys[index.row()] = value

    @Slot(QModelIndex, result=bool)
    def toggle(self, index: QModelIndex, value: Optional[bool] = None) -> bool:
        data = self.data(index)
        if value is None:
            value = not data['checked']
        data['checked'] = value
        self.setData(index, data)
        print(self.data(index))


class Bridge(QObject):
    @Slot(result=bool)
    def isRootUser(self):
        return os.geteuid() == 0

    @Slot(result=bool)
    def hasAcpiCall(self):
        return os.path.isfile("/proc/acpi/call")

    @Slot(str, result=bool)
    def getStatus(self, name):
        return getStatus(name)

    @Slot(result=int)
    def getPerformanceMode(self):
        result = getPerfMode()
        return result.value

    @Slot(int)
    def setPerformanceMode(self, mode):
        print(Mode(mode))
        setPerfMode(Mode(mode))

    @Slot(bool, result=bool)
    def setBatteryConservation(self, val):
        return setBatteryConservation(val)

    @Slot(bool, result=bool)
    def setRapidCharge(self, val):
        return setRapidCharge(val)


# if __name__ == "__main__":
#     listModel = SwitchListModel()
#     idx = listModel.index(0)
#     print(idx.row(), listModel.data(idx))
#     listModel.toggle(idx)
#     print(idx.row(), listModel.data(idx))
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    context = engine.rootContext()
    bridge = Bridge()
    context.setContextProperty("conn", bridge)
    opKeysModel = SwitchListModel()
    # opKeysModel.setStringList(opKeys)
    context.setContextProperty("opKeysModel", opKeysModel)
    qml_file = os.path.join(os.path.dirname(__file__), "view.qml")
    engine.load(qml_file)
    app.setWindowIcon(QIcon(":icons/battery.ico"))
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
