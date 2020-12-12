# This Python file uses the following encoding: utf-8
import sys
import os
from PySide2.QtCore import QObject, QStringListModel, Slot
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QGuiApplication, QIcon
import PySide2.QtQml
from PySide2.QtQuick import QQuickView
from acpi_call import isRapidCharge, isBatteryConservation, getPerfMode, setPerfMode, Mode, setBatteryConservation, setRapidCharge
import icon_rc

opKeys = ["battery conservation mode", "rapid charge"]


class Bridge(QObject):
    @Slot(result=bool)
    def isRootUser(self):
        return os.geteuid() == 0

    @Slot(result=bool)
    def hasAcpiCall(self):
        return os.path.isfile("/proc/acpi/call")

    @Slot(str, result=bool)
    def getStatus(self, name):
        print(f"name: {name}")
        if name == opKeys[0]:
            return isBatteryConservation()
        if name == opKeys[1]:
            return isRapidCharge()

    @Slot(result=int)
    def getPerformanceMode(self):
        result = getPerfMode()
        return result.value

    @Slot(int)
    def setPerformanceMode(self, mode):
        print(Mode(mode))
        setPerfMode(Mode(mode))

    @Slot(bool)
    def setBatteryConservation(self, val):
        setBatteryConservation(val)

    @Slot(bool)
    def setRapidCharge(self, val):
        setRapidCharge(val)


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    context = engine.rootContext()
    bridge = Bridge()
    context.setContextProperty("conn", bridge)
    opKeysModel = QStringListModel()
    opKeysModel.setStringList(opKeys)
    context.setContextProperty("opKeysModel", opKeysModel)
    qml_file = os.path.join(os.path.dirname(__file__), "view.qml")
    engine.load(qml_file)
    app.setWindowIcon(QIcon(":icons/battery.ico"))
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
