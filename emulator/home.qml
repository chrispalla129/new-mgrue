import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.0
import QtQuick.Window 2.1

Window {
    visible: true
    title: "mGRUE"
    color: "lightslategrey"
    property string fileName: ""
    property string statusMessage: ""
    property string buttonMessage: ""
    property QtObject backend

    Connections {
        target: backend
        function onStatus(msg) {
            statusMessage = msg;
        }
    }

    Rectangle {
        id: title
        anchors.fill: parent
        color: "transparent"
        Text {
            text: "mGRUE Device"
            font.family: "Yu Gothic UI Semibold"
            font.pixelSize: 40
            color: "#36454F"
            anchors {
                top: parent.top
                horizontalCenter: parent.horizontalCenter
                topMargin: 12
            }

        }


        Rectangle {
            id: messageSection
            anchors.fill: parent
            color: "transparent"

            Text {
                id: messages
                anchors {
                    bottom: parent.bottom
                    bottomMargin: 12
                    left: parent.left
                    leftMargin: 12
                }
                text: "Status: " + statusMessage
                font.pixelSize: 24
                font.family: "Yu Gothic UI Semilight"
                color: "oldlace"
            }
        }

        Rectangle {
            id: fileLocation
            anchors.fill: parent
            color: "transparent"

            Button {
                id: selectButton
                text: "Start Transfer"
                font.family: "Yu Gothic UI Semilight"
                
                anchors.centerIn: parent
                contentItem: Text {
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    text: selectButton.text
                    color: "oldlace"
                }
                background: Rectangle {
                    implicitWidth: 200
                    implicitHeight: 200
                    color: "#36454F"
                    radius: 8
                }
                onClicked: backend.startTransfer()
            }
        }
        
    }
}
/*##^##
Designer {
    D{i:0;formeditorZoom:0.9}D{i:1}D{i:3}D{i:5}D{i:4}D{i:6}D{i:8}D{i:11}D{i:7}D{i:2}
}
##^##*/