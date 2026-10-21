import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    visible: true
    width: 1100
    height: 700
    minimumWidth: 740
    minimumHeight: 480
    title: "iGPU FilMaker — POC"
    color: "#17191f"

    palette.windowText: "#e6e9ef"
    palette.text: "#e6e9ef"
    palette.buttonText: "#e6e9ef"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12

        Label {
            text: "iGPU FilMaker"
            font.pixelSize: 26
            font.bold: true
            color: "#e6e9ef"
        }

        Label {
            text: "POC-01 · Foundation shell · No media processing yet"
            color: "#a9b0bc"
            font.pixelSize: 13
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#222630"
            radius: 8
            border.color: "#383e4c"

            Column {
                anchors.centerIn: parent
                spacing: 10

                Label {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "Preview"
                    font.pixelSize: 22
                    color: "#e6e9ef"
                }
                Label {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "Media playback arrives in POC-02"
                    color: "#a9b0bc"
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 140
            color: "#222630"
            radius: 8
            border.color: "#383e4c"

            Label {
                anchors.centerIn: parent
                text: "Timeline · coming in POC-03"
                color: "#a9b0bc"
            }
        }
    }
}
