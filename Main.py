import sys
from PyQt5 import QtWidgets, QtCore
from Overlay import Overlay
from Reader import Reader

def main():
    app = QtWidgets.QApplication(sys.argv)

    overlay = Overlay()
    overlay.show()

    reader = Reader()

    def refresh():
        specialPercentage, specialPixelsx = reader.readSpecialMeter()
        heavyPercentage, heavyPixelsx = reader.readHeavylMeter()
        print(specialPercentage)
        overlay.telemRefresh(specialPercentage, heavyPercentage, specialPixelsx, heavyPixelsx)

    timer = QtCore.QTimer()
    timer.timeout.connect(refresh)
    timer.start(1)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    # pyinstaller --onefile --noconsole --icon=resources/icon.ico main.py