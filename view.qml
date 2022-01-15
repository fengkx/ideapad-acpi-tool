import QtQuick 2.2
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.1
import QtQml.Models 2.1

ApplicationWindow {
    id: window
    title: qsTr("IdeaPad ACPI Tool")
    width: 720
    height: 500
    visible: true

    MessageDialog {
        visible: false
        id: messageDialog
        height: 10
        width: 500
        icon: StandardIcon.Critical
        onAccepted: {
            Qt.quit()
        }
        onNo: {
            Qt.quit()
        }

        Component.onCompleted: {
            const isRoot = conn.isRootUser()
            if(!isRoot) {
                title = "Root privileges is required"
                text = "Root privileges is required"
                visible = true
            }
            const hasAcpiCall = conn.hasAcpiCall()
            if(!hasAcpiCall) {
                title = "You need to enable acpi call";
                text = "ACPI Call Module need to be enabled check"
                detailedText = "https://wiki.archlinux.org/index.php/Lenovo_IdeaPad_5_15are05#System_Performance_Mode"
                visible = true
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 20
        anchors.rightMargin: 20
        anchors.leftMargin: 20
        anchors.bottomMargin: 20
        anchors.topMargin: 20
        ListView {
            id: mainView
            height: 150

            anchors.margins: 25
            Layout.maximumHeight: 150
            Layout.preferredHeight: 150
            Layout.margins: 0
            Layout.topMargin: 0
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.fillHeight: false
            Layout.fillWidth: true
            spacing: 20
            model: opKeysModel
            delegate: SwitchRow {}

        }

        Rectangle {
            height: 1
            color: "#aaaaaa"
            border.color: "#aaaaaa"
            anchors.left: parent.left
            anchors.right: parent.right
            Layout.fillHeight: false
        }

        GroupBox {
            id: groupBoxtoggletoggle
            y: 262
            height: 200

            spacing: 6
            padding: 8
            font.pointSize: 16
            Layout.fillHeight: true
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            title: qsTr("Performance Mode")

            background: Rectangle {
                width: parent.width
                height: parent.height - groupBox.topPadding + groupBox.bottomPadding
                anchors.fill: parent
            }

            ListView {
                id: modeListView
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                height: parent.height
                topMargin: 0
                contentX: 0
                model: ["auto", "performance", "battery save"]
                delegate: RadioDelegate {
                    id: radioButton
                    text: modelData
                    width: mainView.width
                    Component.onCompleted: {
                        const result = conn.getPerformanceMode()
                        console.log(result, index)
                        radioButton.checked = result === index
                    }
                    onToggled: {
                        console.log(index, 'onToggled')
                        conn.setPerformanceMode(index)
                    }
                }

            }
        }

    }

}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}
}
##^##*/
