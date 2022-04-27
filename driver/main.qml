import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.0
import QtQuick.Window 2.1

Window {
    visible: true
    width: 800
    height: 600
    title: "mGRUE"
    property string currTime: "00:00:00"
    property string fileName: ""
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

        Button {
            text: "Select Folder"
            width: 200
            height: 50
            x: parent.width / 2 - width / 2         //Centers the x-axis
            y: parent.height / 2 - height / 2       //Centers the y-axis
            onClicked: fileDialog.visible = true    //Opens file dialog on click
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

            Text {
                id: location
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
/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}D{i:1}D{i:3}D{i:4}D{i:5}D{i:7}D{i:8}D{i:2}
}
##^##*/
