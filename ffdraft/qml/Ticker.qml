import QtQuick 1.1

Item {
    width: childrenRect.width; height: childrenRect.height

    signal teamSelected(int index, string name)

    property alias model: teamsModel

    ListModel {
        id: teamsModel
    }

    Component {
        id: teamDelegate

        Column {
            Image {
                width: 48; height: 48
                anchors.horizontalCenter: parent.horizontalCenter
                source: modeldata.img_url

                MouseArea {
                    anchors.fill: parent
                    onClicked: teamSelected(modeldata.index, modeldata.name)
                }
            }
            Text {
                width: 80
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                text: modeldata.name
                clip: true
                elide: Text.ElideRight
            }
        }
    }

    Component {
        id: roundDelegate

        Rectangle {
            height: 48; width: 48
            radius: 10
            gradient: Gradient {
                GradientStop { position: 0.0; color: "grey" }
                GradientStop { position: 1.0; color: "silver" }
            }
            smooth: true

            Text {
                width: parent.width
                id: roundLabel
                color: "white"
                font.bold: true
                anchors.centerIn: parent
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                text: "Round " + modeldata.round
            }
        }
    }

    Component {
        id: teamsDelegate

        Loader {
            id: itemDisplay

            property variant modeldata: teamsModel.get(index)
            sourceComponent: is_round ? roundDelegate : teamDelegate
        }
    }

    Row {
        id: teamsRow
        add: Transition {
            NumberAnimation {
                properties: "x"
                from: width + 100
                easing.type: Easing.OutBounce
                duration: 1000
            }
        }
        move: Transition {
            NumberAnimation {
                properties: "x"
                easing.type: Easing.OutBounce
                duration: 1000
            }
        }
        spacing: 10

        Repeater {
            model: teamsModel
            delegate: teamsDelegate
        }
    }

    function removeTeam(index) {
        teamsModel.remove(index)
    }

    function clearTeams() {
        teamsModel.clear()
    }

    function getTeam(index) {
        return teamsModel.get(index)
    }

    function appendTeam(team) {
        teamsModel.append(team)
    }

    function count() {
        return teamsModel.count
    }

    function isNextRound() {
        return teamsModel.get(1).is_round
    }
}
