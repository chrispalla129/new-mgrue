import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.0

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "mGRUE"
    property string currTime: "00:00:00"
    property QtObject backend

    Connections {
        target: backend

        function onUpdated(msg) {
        currTime = msg;
        }
    }

    Rectangle {
        anchors.fill: parent

        Image {
            anchors.fill: parent
            source: "./images/green_background.jpg"
            fillMode: Image.PreserveAspectCrop
        }

        Rectangle {
            anchors.fill: parent
            color: "transparent"

            Text {
                anchors {
                    bottom: parent.bottom
                    bottomMargin: 12
                    right: parent.right
                    rightMargin: 12
                }
                text: currTime  // display current time
                font.pixelSize: 24
                color: "white"
            }
        }

        FileDialog {
            id: fileDialog
            title: "Please choose desired folder location"
            folder: shortcuts.home
            selectFolder: true
            onAccepted: {
                console.log("You chose: " + fileDialog.fileUrls)
                folderLocation = fileDialog.fileUrls
                close()
            }
            onRejected: {
                console.log("Canceled")
                close()
            }
            Component.onCompleted: visible = true
        }
        Rectangle {
            anchors.fill: parent
            color: "transparent"

            Text {
                anchors {
                    bottom: parent.bottom
                    bottomMargin: 12
                    left: parent.left
                    leftMargin: 12
                }
                text: "destination folder"  // display current destination
                font.pixelSize: 24
                color: "white"
            }
        }
    }
}