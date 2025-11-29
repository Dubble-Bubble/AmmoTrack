import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets

def resource_path(relativePath):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativePath)
    return os.path.join(os.path.abspath("."), relativePath)

class Overlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.Tool
            | QtCore.Qt.WindowTransparentForInput
        )

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.label = QtWidgets.QLabel("defTelem", self)
        self.label.setStyleSheet("""
            color: white; font-size: 15px; font-weight: bold;
            background-color: rgba(0, 0, 0, 150);
            border: 2px solid rgba(255, 255, 255, 200);
            border-radius: 10px;
            """)
        self.label.move(700, 900)

        screen = QtWidgets.QApplication.primaryScreen()
        size = screen.size()
        self.setGeometry(0, 0, size.width(), size.height())

        iconPath = resource_path("resources/app.ico")
        icon = QtGui.QIcon(iconPath)
        self.tray_icon = QtWidgets.QSystemTrayIcon(icon, self)
        menu = QtWidgets.QMenu()
        quit_action = menu.addAction("Quit Overlay")
        quit_action.triggered.connect(QtWidgets.QApplication.quit)
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()
        self.label.resize(300, 80)   

    def telemRefresh(self, specialMeter, heavyMeter, specialPixels, heavyPixels) :
        self.label.setText(f"Special Meter %: {specialMeter}\nSPMeter Px / 96: {specialPixels}\nHeavy Meter %: {heavyMeter}\nHMeter Px / 96: {heavyPixels}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()

    sys.exit(app.exec_())