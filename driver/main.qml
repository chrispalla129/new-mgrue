import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.0
import QtQuick.Window 2.1

Window {
    visible: true
    width: 600
    height: 500
    title: "mGRUE"
    color: "lightslategrey"
    property string fileName: ""
    property string statusMessage: ""
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
            text: "mGRUE Host Device Driver"
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
                color: "oldlace"
            }
        }


        FileDialog {
            id: fileDialog
            visible: false
            title: "Please choose desired folder location"
            folder: shortcuts.home
            selectFolder: true
            onAccepted: {
                backend.getFileLocation(fileDialog.fileUrls)
                location.text = fileDialog.fileUrls[0]
                fileName = fileDialog.fileUrls[0]
                close()
            }
            onRejected: {
                console.log("File selection canceled by user")
                close()
            }
        }
        Rectangle {
            id: fileLocation
            anchors.fill: parent
            color: "transparent"

            Button {
            id: selectButton
            text: "Select Folder"
            
            anchors.centerIn: parent
            contentItem: Text {
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: selectButton.text
                color: "lightsteelblue"
            }
            background: Rectangle {
                implicitWidth: 200
                implicitHeight: 50
                color: "#36454F"
                radius: 8
            }
            onClicked: fileDialog.visible = true    //Opens file dialog on click
        }

            Text {
                id: location
                anchors {
                    top: selectButton.bottom
                    topMargin: 12
                    left: selectButton.left
                    leftMargin: 12
                }
                text: "destination folder"  // display current destination
                font.pixelSize: 24
                color: "oldlace"
            }
        }
    }
}
/*##^##
Designer {
    D{i:0;formeditorZoom:0.33}D{i:1}D{i:4}D{i:3}D{i:5}D{i:7}D{i:6}D{i:8}D{i:10}D{i:9}
D{i:2}
}
##^##*/
