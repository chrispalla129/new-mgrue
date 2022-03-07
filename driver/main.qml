import QtQuick 2.15
import QtQuick.Controls 2.15

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

    }

}