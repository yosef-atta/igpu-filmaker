import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import QtMultimedia

ApplicationWindow {
    id: window
    visible: true
    width: 1180
    height: 760
    minimumWidth: 800
    minimumHeight: 550
    title: "iGPU FilMaker — POC-02 Media Playback"
    color: "#17191f"

    palette.windowText: "#e6e9ef"
    palette.text: "#e6e9ef"
    palette.buttonText: "#e6e9ef"

    FileDialog {
        id: mediaDialog
        title: "Import media"
        fileMode: FileDialog.OpenFiles
        nameFilters: ["Media files (*.mp4 *.mov *.mkv *.webm *.mp3 *.wav *.m4a)", "All files (*)"]
        onAccepted: {
            for (let i = 0; i < selectedFiles.length; i++) {
                mediaController.importFile(selectedFiles[i].toString())
            }
        }
    }

    AudioOutput {
        id: audioOutput
        volume: volumeSlider.value
    }

    MediaPlayer {
        id: player
        audioOutput: audioOutput
        videoOutput: videoOutput
        onErrorOccurred: function(error, errorString) {
            if (error !== MediaPlayer.NoError) {
                mediaController.reportPlaybackError(errorString)
            }
        }
        onMediaStatusChanged: {
            if (mediaStatus === MediaPlayer.LoadedMedia || mediaStatus === MediaPlayer.BufferedMedia) {
                mediaController.reportPlaybackBackend(
                    "Source ready in Qt Multimedia (actual hardware decoder is not reported)")
            }
            if (mediaStatus === MediaPlayer.InvalidMedia) {
                mediaController.reportPlaybackError("Unsupported or invalid media")
            }
        }
    }

    function timeString(milliseconds) {
        const seconds = Math.max(0, Math.floor(milliseconds / 1000))
        const minutes = Math.floor(seconds / 60)
        const hours = Math.floor(minutes / 60)
        return String(hours).padStart(2, "0") + ":" +
               String(minutes % 60).padStart(2, "0") + ":" +
               String(seconds % 60).padStart(2, "0")
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 10

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: "iGPU FilMaker"
                font.pixelSize: 25
                font.bold: true
                color: "#e6e9ef"
            }
            Label {
                text: "POC-02 · Source preview"
                color: "#a9b0bc"
                Layout.leftMargin: 12
            }
            Item { Layout.fillWidth: true }
            Button {
                text: "Import Media"
                onClicked: mediaDialog.open()
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 12

            Rectangle {
                Layout.preferredWidth: 295
                Layout.fillHeight: true
                color: "#222630"
                radius: 8
                border.color: "#383e4c"

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 12
                    spacing: 8

                    Label {
                        text: "PROJECT MEDIA"
                        font.bold: true
                        color: "#e6e9ef"
                    }
                    Label {
                        text: mediaController.items.length + " imported"
                        color: "#a9b0bc"
                    }
                    ListView {
                        id: mediaList
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true
                        model: mediaController.items
                        spacing: 5
                        delegate: Rectangle {
                            required property var modelData
                            width: mediaList.width
                            height: 64
                            radius: 5
                            color: mouseArea.containsMouse ? "#3d4957" : "#303744"
                            Column {
                                anchors.fill: parent
                                anchors.margins: 8
                                spacing: 5
                                Label {
                                    text: modelData.name
                                    width: parent.width
                                    elide: Text.ElideRight
                                    color: "#e6e9ef"
                                }
                                Label {
                                    text: modelData.details
                                    width: parent.width
                                    elide: Text.ElideRight
                                    font.pixelSize: 11
                                    color: "#abb9c7"
                                }
                            }
                            MouseArea {
                                id: mouseArea
                                anchors.fill: parent
                                hoverEnabled: true
                                onClicked: {
                                    player.stop()
                                    player.source = modelData.url
                                    player.play()
                                }
                            }
                        }
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: "#222630"
                radius: 8
                border.color: "#383e4c"

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 12
                    spacing: 8

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        color: "#080a0e"

                        VideoOutput {
                            id: videoOutput
                            anchors.fill: parent
                            fillMode: VideoOutput.PreserveAspectFit
                        }

                        Label {
                            anchors.centerIn: parent
                            visible: player.source.toString() === ""
                            text: "Import media, then click a file to preview"
                            color: "#a9b0bc"
                        }
                    }

                    Slider {
                        id: seekSlider
                        Layout.fillWidth: true
                        from: 0
                        to: Math.max(player.duration, 1)
                        value: player.position
                        enabled: player.seekable
                        onMoved: player.setPosition(value)
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        Button {
                            text: player.playbackState === MediaPlayer.PlayingState ? "Pause" : "Play"
                            enabled: player.source.toString() !== ""
                            onClicked: {
                                if (player.playbackState === MediaPlayer.PlayingState) player.pause()
                                else player.play()
                            }
                        }
                        Button {
                            text: "Stop"
                            enabled: player.source.toString() !== ""
                            onClicked: player.stop()
                        }
                        Label {
                            text: timeString(player.position) + " / " + timeString(player.duration)
                            color: "#e6e9ef"
                        }
                        Item { Layout.fillWidth: true }
                        Label { text: "Volume"; color: "#a9b0bc" }
                        Slider {
                            id: volumeSlider
                            Layout.preferredWidth: 100
                            from: 0
                            to: 1
                            value: 0.75
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 95
            color: "#222630"
            radius: 8
            border.color: "#383e4c"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 12
                Label {
                    text: "Timeline editing is scheduled for POC-03"
                    color: "#a9b0bc"
                }
                Label {
                    Layout.fillWidth: true
                    text: mediaController.status
                    color: "#e6e9ef"
                    elide: Text.ElideRight
                }
                Label {
                    Layout.fillWidth: true
                    text: "FFmpeg hardware interfaces: " + mediaController.hardwareReport
                    color: "#a9b0bc"
                    elide: Text.ElideRight
                    font.pixelSize: 11
                }
            }
        }
    }
}
