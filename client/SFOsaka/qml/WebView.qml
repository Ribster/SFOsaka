import QtQuick 2.4
import QtQuick.Controls 1.4
import QtWebView 1.1
import QtQuick.Layouts 1.3

// Originally had this in a layout in an item, but that doesn't work,
// so just put layout as the root (in this component).
ColumnLayout {
    id: root
    property string url

    signal buttonActivated()

    AppBar {
        id: toolbar
        onButtonActivated: {
            stackView.pop()
        }
    }

    WebView {
        id: webView
        Layout.alignment: Qt.AlignTop
        Layout.fillWidth: true
        Layout.fillHeight: true
        url: root.url
    }

}
