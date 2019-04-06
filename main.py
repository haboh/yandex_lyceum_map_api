import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from object_size import get_dlan_dlat
from random import randrange
from toponym import find_toponym_coordinates, find_district_by_coordinates

MAP_URL = 'https://static-maps.yandex.ru/1.x/'
FILENAME = "map.png"
LL = 37.620070, 55.753630


class MapsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Yandex map')
        self.setGeometry(0, 0, 600, 450)
        self.pixMap = QLabel(self)
        self.scale = 10
        self.ll = LL

    def update_map(self, t="map"):
        params = {
            "ll": ','.join(map(str, self.ll)),
            "l": t,
            "z": str(self.scale),
        }
        response = requests.get(MAP_URL, params=params)
        with open(FILENAME, "wb") as file:
            file.write(response.content)
        assert response
        pixmap = QPixmap(FILENAME)
        self.pixMap.setPixmap(pixmap)
        self.pixMap.resize(pixmap.size())

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_PageUp:
            self.scale += 1
        if e.key() == Qt.Key_PageDown:
            self.scale -= 1
        self.scale = min(max(self.scale, 0), 17)
        self.update_map()


def main():
    app = QApplication(sys.argv)
    ex = MapsMainWindow()
    ex.show()
    ex.update_map()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
