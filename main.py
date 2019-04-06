import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from object_size import get_dlan_dlat
from random import randrange
from toponym import find_toponym_coordinates, find_district_by_coordinates

MAP_URL = 'https://static-maps.yandex.ru/1.x/'
FILENAME = "map.png"
SCALE = 1


class MapsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Yandex map')
        self.setGeometry(0, 0, 600, 450)
        self.pixMap = QLabel(self)

    def update_map(self, ll, spn=(0.01, 0.01), t="map"):
        params = {
            "ll": ','.join(map(str, ll)),
            "spn": ','.join(map(str, spn)),
            "l": t,
            "z": str(SCALE),
        }
        response = requests.get(MAP_URL, params=params)
        with open(FILENAME, "wb") as file:
            file.write(response.content)
        assert response
        pixmap = QPixmap(FILENAME)
        self.pixMap.setPixmap(pixmap)
        self.pixMap.resize(pixmap.size())


def main():
    app = QApplication(sys.argv)
    ex = MapsMainWindow()
    ex.show()
    ex.update_map((60, 60))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
