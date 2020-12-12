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
    text: opKeysModel.data(opKeysModel.index(index, 0))
    width: mainView.width
    onToggled: {
        if(index === 0) {
            conn.setBatteryConservation(control.checked)
        }
        else if (index === 1) {
            conn.setRapidCharge(control.checked)
        }

    }
    Component.onCompleted: {
        const result = conn.getStatus(control.text)
        console.log(result)
        control.checked = result
    }
}
