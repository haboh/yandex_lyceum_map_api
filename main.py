# ------------------------------------------------------ #
# github: https://github.com/haboh/yandex_lyceum_map_api #
# ------------------------------------------------------ #
import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from object_size import get_dlan_dlat
from random import randrange
from toponym import find_toponym_coordinates, find_district_by_coordinates, NotFoundError

MAP_URL = 'https://static-maps.yandex.ru/1.x/'
FILENAME = "map"
LL = [37.620070, 55.753630]
MAPTYPES = ['map', 'satelite', 'hybrid']
MAPTYPESSHORT = ['map', 'sat', 'sat,skl']


class MapsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.marked_objects = []
        self.type = 0
        self.setWindowTitle('Yandex map')
        self.setGeometry(0, 0, 600, 520)
        self.pixMap = QLabel(self)
        self.typeLabel = QLabel(self)
        self.typeLabel.setText('Map type')
        self.typeButton = QPushButton(MAPTYPES[self.type], self)
        self.typeButton.move(0, 490)
        self.typeLabel.move(20, 460)
        self.searchLineLabel = QLabel(self)
        self.searchLineLabel.move(130, 460)
        self.searchLineLabel.setText('Object')
        self.searchLine = QLineEdit(self)
        self.searchLine.move(120, 490)
        self.searchLine.resize(200, 20)
        self.searchButton = QPushButton(self)
        self.searchButton.setText('Search')
        self.searchButton.move(330, 490)
        self.searchButton.clicked.connect(self.search_object)
        self.typeButton.clicked.connect(self.change_type)
        self.scale = 3
        self.ll = LL
        self.resetButton = QPushButton(self)
        self.resetButton.setText('Reset')
        self.resetButton.move(430, 490)
        self.resetButton.clicked.connect(self.clear_marked_objects)

    def clear_marked_objects(self):
        self.marked_objects = []
        self.update_map()

    def search_object(self):
        object_name = self.searchLine.text()
        previous_ll = self.ll
        previous_scale = self.scale
        try:
            ll = find_toponym_coordinates(object_name)
            self.ll = ll
            self.scale = 17
            self.marked_objects = [ll]
            self.update_map()
        except NotFoundError:
            self.ll = previous_ll
            self.scale = previous_scale
            self.searchLine.setText('Object not found')
        except AssertionError:
            self.ll = previous_ll
            self.scale = previous_scale
            self.searchLine.setText('Cordinates error')
        except Exception as e:
            self.ll = previous_ll
            self.scale = previous_scale
            self.searchLine.setText('Undefined error')
            print(e)

    def change_type(self):
        self.type = (self.type + 1) % 3
        self.typeButton.setText(MAPTYPES[self.type])
        self.update_map()

    def update_map(self):
        params = {
            "ll": ','.join(map(str, self.ll)),
            "l": MAPTYPESSHORT[self.type],
            "z": str(self.scale),
            "pt": '~'.join(map(lambda x: str(x[0]) + ',' + str(x[1]), self.marked_objects)),
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
