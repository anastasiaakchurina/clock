import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Clock(QMainWindow):

    def __init__(self):
        super().__init__()

        self.countries = [
            'Russia',
            'USA',
            'France',
        ]

        self.cities = [
            [
                'Moscow',
                'Samara',
            ],
            [
                'Washington',
                'Dallas',
            ],
            [
                'Paris',
            ],
        ]

        self.zones = [
            [
                -1,
                0,
            ],
            [
                -9,
                -10,
            ],
            [
                -3,
            ],
        ]

        self.initUI()

    def initUI(self):
        self.lbl = QLabel('', self)
        self.lbl.move(20, 80)
        self.lbl.resize(150, 20)

        self.alert = False

        self.radio_button_12 = QRadioButton('12', self)
        self.radio_button_24 = QRadioButton('24', self)
        self.radio_button_12.move(15, 110)
        self.radio_button_24.move(15, 130)

        self.radio_button_12.setChecked(True)

        self.timeFormat = QButtonGroup(self)
        self.timeFormat.addButton(self.radio_button_12)
        self.timeFormat.addButton(self.radio_button_24)

        self.radio_button_d1 = QRadioButton('dd.mm.yy', self)
        self.radio_button_d2 = QRadioButton('mm-dd-yy', self)
        self.radio_button_d1.move(60, 110)
        self.radio_button_d2.move(60, 130)

        self.radio_button_d1.setChecked(True)

        self.dateFormat = QButtonGroup(self)
        self.dateFormat.addButton(self.radio_button_d1)
        self.dateFormat.addButton(self.radio_button_d2)

        self.dateFormat.buttonClicked.connect(self.showTime)

        country = QComboBox(self)
        country.addItems(
            self.countries
        )
        country.move(10, 10)
        country.activated[str].connect(self.onCountyActivated)
        self.country = country

        city = QComboBox(self)
        city.addItems(
            self.cities[0]
        )
        city.move(10, 40)
        self.city = city

        submit = QPushButton('OK', self)
        submit.clicked.connect(self.addAlert)
        submit.move(300, 10)

        alertTime = QTimeEdit(QTime.currentTime(), self)
        alertTime.move(200, 10)
        self.alertTime = alertTime

        alertMessage = QPlainTextEdit('', self)
        alertMessage.move(200, 50)
        alertMessage.resize(200, 60)
        self.alertMessage = alertMessage

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()

        self.resize(400, 160)
        self.center()
        self.setWindowTitle('Clock')
        self.show()

    def onCountyActivated(self):
        self.city.clear()
        self.city.addItems(
            self.cities[self.country.currentIndex()]
        )

    def addAlert(self):
        self.alert = True

    def showTime(self):
        time = QDateTime.currentDateTime()
        if self.dateFormat.checkedId() == -2:
            format = 'dd.mm.yy '
        else:
            format = 'mm-dd-yy '
        if self.timeFormat.checkedId() == -3:
            format += 'hh:mm:ss'
        else:
            format += 'h:m:s ap'

        zone = self.zones[self.country.currentIndex()][self.city.currentIndex()]

        text = time.addSecs(3600 * zone).toString(format)

        if self.alert and time.addSecs(3600 * zone).toString('hh:mm') == self.alertTime.time().toString('hh:mm'):
            self.alert = False
            self.exPopup = alertPopup(self.alertMessage.toPlainText())
            self.exPopup.setGeometry(100, 200, 100, 100)
            self.exPopup.show()
            self.exPopup.center()

        self.lbl.setText(text)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


class alertPopup(QWidget):
    def __init__(self, name):
        super().__init__()

        self.name = name

        self.initUI()

    def initUI(self):
        lblName = QLabel(self.name, self)
        lblName.move(10, 10)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QApplication([])
    clock = Clock()
    sys.exit(app.exec_())
