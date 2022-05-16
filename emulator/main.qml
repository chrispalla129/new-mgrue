import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.0
import QtQuick.Window 2.1

ApplicationWindow {
    id: window
    visible: true
    visibility: "FullScreen"
    width: 480
    height: 320

    title: "mGRUE"
    color: "lightslategrey"
    property string fileName: ""
    property string statusMessage: ""
    property string buttonMessage: ""
    property int transferSpeed: 5
    property QtObject backend

    Connections {
        target: backend
        function onStatus(msg) {
            statusMessage = msg;
        }
        function onSpeed(speed) {
            transferSpeed = speed;
        }
    }

    function getButtonMessage() {
        var stat = statusMessage
        console.log(statusMessage)
        if(stat == "Awaiting Connection" || stat == "Attempting to Connect..." || stat == "ERROR: Serial port connection error!" || stat == "ERROR: File read error!"){
            return "Connect"
        }
        else if(stat == "Paused" || stat =="Paused.") {
            return "Resume"
        }
        else if(stat == "Connected" || stat == "Finished Transfer" || stat == "User stopped transfer early"){
            return "Start Transfer"
        }
        if (stat == "Connected, transferring....") {
            return "Pause"
        }


    }
    function slowerAllowed() {
        var speed = transferSpeed
        if(speed > 1){
            return true
        }
        else {
            return false
        }
    }
    function fasterAllowed() {
        var speed = transferSpeed
        if(speed < 5){
            return true
        }
        else {
            return false
        }
    }


    function toggleScreen() {
        if(window.visibility == 5|| window.visibility ==4){
            window.visibility = "Windowed"
        }
        else if(window.visibility == 2){
            window.visibility = "FullScreen"
        }
    }
    Button {
        id: toggle
        anchors{
            top: parent.top
            topMargin: 4
            right: parent.right
            rightMargin: 4
        }
        background: Rectangle{
            color: "#36454F"
            implicitHeight: 40
            implicitWidth: 100
            radius: 4
        }
        contentItem: Text{
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "oldlace"
            text: "Toggle Screen"
        }
        
        onClicked: toggleScreen()
    }

    Rectangle {
        id: title
        anchors.fill: parent
        color: "transparent"
        Text {
            id: titleText
            text: "mGRUE"
            font.family: "Yu Gothic UI Semibold"
            font.pixelSize: 40
            color: "oldlace"
            anchors {
                top: parent.top
                horizontalCenter: parent.horizontalCenter
            }
        }

        FileDialog {
            id: fileDialog
            visible: false
            title: "Please choose desired source file"
            folder: shortcuts.home
            onAccepted: {
                //update directory where files should be read from
                backend.getFileLocation(fileDialog.fileUrls)
                //location.text = fileDialog.fileUrls[0]
                fileName = fileDialog.fileUrls[0]
                console.log("User selected: "+ fileDialog.fileUrls[0])
                close()
            }
            onRejected: {
                console.log("File selection canceled by user")
                close()
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
            id: speeds
            color: "transparent"
            anchors {
                left: parent.horizontalCenter
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }
            Rectangle {
                id: displaySpeed
                anchors{
                    bottom: increaseSpeed.top
                    bottomMargin: 50
                    horizontalCenter: parent.horizontalCenter
                    horizontalCenterOffset: -5
                }
                Text{
                    text: transferSpeed
                    color: "oldlace"
                    font.pixelSize: 32
                    font.family: "Yu Gothic UI Semibold"
                }
                color: "transparent"

            }
            Button {
                id: increaseSpeed
                text: "+"
                font.pixelSize: 48
                anchors{
                    left: parent.horizontalCenter
                    leftMargin:5
                    verticalCenter: parent.verticalCenter
                }
                contentItem: Text {
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    text: increaseSpeed.text
                    color: "oldlace"
                    font.pixelSize: 48
                }
                background: Rectangle {
                    implicitWidth: 105
                    implicitHeight: 105
                    color: increaseSpeed.pressed ? "dimgrey" : !enabled  ? "dimgrey" :"#36454F"
                    radius: 8
                }
                enabled: fasterAllowed()

                onClicked: backend.upSpeed()

            }
            Button {
                id: decreaseSpeed
                text: "-"
                font.pixelSize: 48

                anchors{
                    right: parent.horizontalCenter
                    leftMargin: 5
                    verticalCenter: parent.verticalCenter
                }
                contentItem: Text {
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    text: decreaseSpeed.text
                    color: "oldlace"
                    font.pixelSize: 48
                }
                background: Rectangle {
                    implicitWidth: 105
                    implicitHeight: 105
                    color: decreaseSpeed.pressed ? "dimgrey" : !enabled  ? "dimgrey" :"#36454F"
                    radius: 8
                }
                enabled: slowerAllowed()
                onClicked: backend.downSpeed()
            }
        }
        Rectangle {
            id: transfer
            anchors{
                right: parent.horizontalCenter
                top: parent.top
                bottom: parent.bottom
                left: parent.left
            }
            color: "transparent"

            Button{
            id: settingsButton
            text: "Stop Transfer"
            font.family: "Yu Gothic UI Semilight"
            anchors {
                top: selectButton.bottom
                topMargin: 5
                left: selectButton.left
            }
            contentItem: Text {
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: settingsButton.text
                color: "oldlace"
                font.pixelSize: 24
            }
            background: Rectangle {
                implicitWidth: 150
                implicitHeight: 100
                color: settingsButton.pressed ? "dimgrey" :"#36454F"
                radius: 8
            }
            onClicked: backend.stopTransfer()
        }
        Button {
            id: selectButton
            text: getButtonMessage()
            font.family: "Yu Gothic UI Semilight"

            anchors{
                bottom: parent.verticalCenter
                bottomMargin: 5
                horizontalCenter: parent.horizontalCenter
            }
            contentItem: Text {
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: selectButton.text
                color: "oldlace"
                font.pixelSize: 24
            }
            background: Rectangle {
                implicitWidth: 150
                implicitHeight: 100
                color: selectButton.pressed ? "dimgrey" :"#36454F"
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
