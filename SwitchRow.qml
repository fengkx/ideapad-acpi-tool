import QtQuick 2.0
import QtQuick.Controls 2.15

SwitchDelegate {
    id: control
    contentItem: Text {
        id: itemContent
        text: control.text
        opacity: enabled ? 1.0 : 0.3
        elide: Text.ElideRight
        verticalAlignment: Text.AlignVCenter
        font.family: "Noto Sans, Times New Roman,Arial"
        font.pointSize: 14
        minimumPointSize: 14
        minimumPixelSize: 18
    }
    visible: true
    checked: opKeysModel.data(opKeysModel.index(index, 0)).checked
    text: opKeysModel.data(opKeysModel.index(index, 0)).text
    width: mainView.width
    onToggled: {
        if(index === 0) {
            const isRapidCharge = conn.setRapidCharge(!control.checked)
            const isBatteryConservation = conn.setBatteryConservation(control.checked)
            opKeysModel.toggle(opKeysModel.index(index, 0), isBatteryConservation)
            opKeysModel.toggle(opKeysModel.index(1, 0), isRapidCharge)
        }
        else if (index === 1) {
            conn.setBatteryConservation(!control.checked)
            conn.setRapidCharge(control.checked)
        }

    }
}
