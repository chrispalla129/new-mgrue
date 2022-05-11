import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.0
import QtQuick.Window 2.1

Window {
    visible: true
    width: 480
    height: 320
    title: "mGRUE"
    color: "lightslategrey"
    property string fileName: ""
    property string statusMessage: ""
    property string buttonMessage: ""
    property string transferSpeed: ""
    property QtObject backend

    Connections {
        target: backend
        function onStatus(msg) {
            statusMessage = msg;
        }
    }

    function getButtonMessage() {
        var stat = statusMessage
        if(stat = "Awaiting Connection"){
            return "Connect"
        }
        else if(stat = "Paused") {
            return "Resume"
        }
        else if(stat = "Connected"){
            return "Start Transfer"
        }
            
    }
    function slowerAllowed() {
        var speed = transferSpeed
        if(speed >1){
            return true
        }
        else {
            return false
        }
    }
    function fasterAllowed() {
        var speed = transferSpeed
        if(speed <5){
            return true
        }
        else {
            return false
        }
    }

    Rectangle {
        id: title
        anchors.fill: parent
        color: "transparent"
        Text {
            id: titleText
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

        FileDialog {
            id: fileDialog
            visible: false
            title: "Please choose desired folder location"
            folder: shortcuts.home
            selectFolder: true
            onAccepted: {
                //update directory where files should be read from
                //backend.getFileLocation(fileDialog.fileUrls)
                //location.text = fileDialog.fileUrls[0]
                //fileName = fileDialog.fileUrls[0]
                console.log("User selected: "+ fileDialog.fileUrls[0])
                close()
            }
            onRejected: {
                console.log("File selection canceled by user")
                close()
            }
        }
        Button{
            id: settingsButton
            text: "Settings"
            font.family: "Yu Gothic UI Semilight"
            anchors {
                top: titleText.top
                topMargin: 5
                right: titleText.left
                rightMargin: 25
            }
            contentItem: Text {
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: settingsButton.text
                color: "oldlace"
            }
            background: Rectangle {
                implicitWidth: 50
                implicitHeight: 50
                color: "#36454F"
                radius: 8
            }
            onClicked: fileDialog.visible = true
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
            id: speeds
            color: "red"
            anchors {
                left: parent.horizontalCenter
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }

            Button {
                text: "+"
            }
        }
        Rectangle {
            id: transfer
            anchors.fill: parent
            color: "transparent"

            Button {
                id: selectButton
                text: getButtonMessage()
                font.family: "Yu Gothic UI Semilight"
                
                anchors.centerIn: parent
                contentItem: Text {
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    text: selectButton.text
                    color: "oldlace"
                }
                background: Rectangle {
                    implicitWidth: 50
                    implicitHeight: 50
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
