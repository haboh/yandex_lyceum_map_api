# ------------------------------------------------------ #
# github: https://github.com/haboh/yandex_lyceum_map_api #
# ------------------------------------------------------ #

import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from object_size import get_dlan_dlat
from random import randrange
from toponym import find_toponym_coordinates, find_district_by_coordinates

MAP_URL = 'https://static-maps.yandex.ru/1.x/'
FILENAME = "map"
LL = [37.620070, 55.753630]
MAPTYPES = ['map', 'satelite', 'hybrid']
MAPTYPESSHORT = ['map', 'sat', 'sat,skl']


class MapsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.type = 1
        self.setWindowTitle('Yandex map')
        self.setGeometry(0, 0, 700, 450)
        self.pixMap = QLabel(self)
        self.typeLabel = QLabel(self)
        self.typeLabel.setText('Map type')
        self.typeButton = QPushButton(MAPTYPES[self.type], self)
        self.typeButton.move(600, 30)
        self.typeLabel.move(625, 0)
        self.typeButton.clicked.connect(self.change_type)
        self.scale = 3
        self.ll = LL

    def change_type(self):
        self.type = (self.type + 1) % 3
        self.typeButton.setText(MAPTYPES[self.type])
        self.update_map()

    def update_map(self):
        params = {
            "ll": ','.join(map(str, self.ll)),
            "l": MAPTYPESSHORT[self.type],
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
        delta = 360 / (2 ** self.scale)
        previous_ll = self.ll
        if e.key() == Qt.Key_PageUp:
            self.scale += 1
        if e.key() == Qt.Key_PageDown:
            self.scale -= 1
        if e.key() == Qt.Key_Left:
            self.ll[0] -= delta
        if e.key() == Qt.Key_Right:
            self.ll[0] += delta
        if e.key() == Qt.Key_Up:
            self.ll[1] += delta
        if e.key() == Qt.Key_Down:
            self.ll[1] -= delta
        self.scale = min(max(self.scale, 0), 17)
        try:
            self.update_map()
        except AssertionError:
            self.ll = previous_ll


def main():
    app = QApplication(sys.argv)
    ex = MapsMainWindow()
    ex.show()
    ex.update_map()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
