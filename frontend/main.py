from PyQt5 import QtSerialPort, QtCore
from PyQt5.QtCore import QTimer, QTime, Qt, pyqtSignal, pyqtSlot, \
        QObject, QThread
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, \
        QTableWidgetItem, QHeaderView, QTableWidget, \
        QStatusBar, QAction, QDialog
# from PyQt5.QtSerialPort import QSerialPortInfo
from datetime import datetime
from dateutil import parser
import serial
import sys
import time

# custom imports
from interface import Ui_MainWindow
from dialog import Ui_Form as Form
from api import carmodels_url, officers_url, carmovements_url, \
    enter_url, exit_url, specific_carmodel_url, \
    handle_get_requests, handle_post_movement, getlastcar_url, \
    inside_url, outside_url

from serial_list import serial_ports


class SerialPort(QObject):
    def __init__(self, parent = None):
        super(SerialPort, self).__init__(parent)

    # Explicit signal
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    working = pyqtSignal(str)

    @pyqtSlot(str)
    def ReadSerialPort(self, port):
        #initialization and open the port
        print(port)
        self.ser = serial.Serial(port, 9600)
        print("Connecting device...")
        self.progress.emit("TEST")
        # self.finished.emit()
        self.working.emit("TEST")

    @pyqtSlot()
    def run(self):
        # while True:
        #     try:
        data = self.ser.readline().decode("UTF")
        self.ser.flushInput()
        data = data[:-2]
        # print(data)
        time.sleep(0.3)
        self.working.emit(data)
        # self.finished.emit()
        self.progress.emit(data)
        # time.sleep(0.5)
        # except:
        #     print("Processing...")
        #     break

        if self.ser.isOpen() == False:
            print("Serial Port is Close")


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setGeometry(10, 10, 1366, 768)

        self.menu_bar()
        self.layouts()
        self.show()
        self.update_table()
        self.auto_connect_arduino()

    def menu_bar(self):
        self.bar = self.menuBar()
        self.menu = self.bar.addMenu("Rashod")

        self.calc = self.menu.addAction("Hasap")
        self.calc.triggered.connect(self.calculate)

    def auto_connect_arduino(self):
        ports = serial_ports()
        for port in ports:
            try:
                ser = serial.Serial(port, 9600)
                self.connect(port)
            except serial.serialutil.SerialException:
                print("Arduino not connected")

    def calculate(self):
        dlg = QDialog()
        dlg.ui = Form()
        dlg.ui.setupUi(dlg)
        dlg.setGeometry(10, 10, 1366, 768)


        output = self.consumption()
        # time.sleep(1)
        self.update_inside(dlg.ui, output)
        self.update_outside(dlg.ui, output)
        dlg.exec_()
        dlg.show()

    def consumption(self):
        in_and_out = []
        cars = handle_get_requests(carmodels_url)
        # print(cars)
        for car in cars:
            obj = {}
            _ = handle_get_requests(getlastcar_url, car['id'])
            if _ == []:
                obj['id'] = car['id']
                obj['license_number'] = car['license_number']
                obj['model_car'] = car['model_car']
                obj['movement'] = 'Girdi'
            else:
                obj['id'] = _[0]['car']['id']
                obj['license_number'] = car['license_number']
                obj['model_car'] = car['model_car']
                obj['movement'] = _[0]['movement']
            in_and_out.append(obj)

        return in_and_out

    def layouts(self):
        # self.last_moved_car()
        self.show_clock()
        self.update_entry()
        self.update_exit()
        # self.connect()

    def connect(self, port):
        # Read Selected Serial Port
        self.serialThread = QThread()
        self.ser = SerialPort()
        self.ser.moveToThread(self.serialThread)
        print(port)
        # port = "/dev/ttyUSB0"
        self.serialThread.started.connect(lambda: self.ser.ReadSerialPort(port))
        self.ser.finished.connect(self.ser.deleteLater)
        self.serialThread.finished.connect(self.serialThread.deleteLater)
        self.serialThread.started.connect(lambda port=port: self.ser.ReadSerialPort(port))
        self.ser.progress.connect(self.ser.run)
        self.ser.working[str].connect(lambda data: self.last_moved_car(data))
        self.serialThread.start()

        self.rfid = ''
        self.start_time = 0

    def parse_date(self, movementTime):
        time = parser.parse(movementTime)
        if time.hour < 10:
            hour = "0{}".format(time.hour)
        else:
            hour = time.hour
        if time.minute < 10:
            minute = "0{}".format(time.minute)
        else:
            minute = time.minute
        if time.second < 10:
            second = "0{}".format(time.second)
        else:
            second = time.second
        return "{0}:{1}:{2}".format(hour, minute, second)

    @pyqtSlot()
    def last_moved_car(self, carRFID):
        import time as systime
        if self.rfid == carRFID:
            if systime.time() - self.start_time < 1:
                return
        print("LAST Moved: ", carRFID)
        # post info to server
        car = handle_get_requests(specific_carmodel_url, carRFID)
        if not car:
            return
        # print(car)
        last_movement = handle_get_requests(getlastcar_url, car[0]["id"])
        if last_movement == []:
            movement = handle_post_movement("Çykdy", carRFID)
        elif last_movement[0]["movement"] == "Çykdy":
            movement = handle_post_movement("Girdi", carRFID)
        else:
            movement = handle_post_movement("Çykdy", carRFID)
        # print("Movement: ")
        # print(movement)

        # update info
        self.ui.model_car.setText(car[0]["model_car"])
        self.ui.license_plate.setText(car[0]["license_number"])
        if movement["movement"] == "Girdi":
            self.ui.movement.setText("GIRDI")
            self.ui.movement.setStyleSheet(
                "color:green; \
                font-size:24; \
                font-weight: bold;")
        elif movement["movement"] == "Çykdy":
            self.ui.movement.setText("ÇYKDY")
            self.ui.movement.setStyleSheet(
                "color:red; \
                font-size:24; \
                font-weight: bold;")
        # show time
        time = self.parse_date(movement["time"])
        self.ui.time.setText(time)

        self.rfid = carRFID
        self.start_time = systime.time()
        # print(movement)
        # print(car)

    def show_clock(self):
        # setting clock
        # creating a timer object
        timer = QTimer(self)

        # adding action to timer
        timer.timeout.connect(self.show_time)

        # update the timer every second
        timer.start(1000)

    def update_table(self):
        timer1 = QTimer(self)
        timer2 = QTimer(self)
        # timer_status = QTimer(self)
        # adding action to timer
        timer1.timeout.connect(self.update_entry)
        timer2.timeout.connect(self.update_exit)
        # timer_status.timeout.connect(self.last_moved_car)
        # update the timer every second
        timer1.start(9000)
        timer2.start(9000)
        # timer_status.start(1000)

    # method called by timer
    def show_time(self):
        # getting current time
        current_time = QTime.currentTime()
        # converting QTime object to string
        curr_time = current_time.toString('hh:mm')
        # showing it to the label
        self.ui.lcdNumber.display(curr_time)

        # setting date
        date = datetime.now()
        self.ui.lcdDay.display(date.day)
        self.ui.lcdMonth.display(date.month)
        self.ui.lcdYear.display(date.year)

    def set_color_to_row_entry(self, table, rowIndex, color):
        # for j in range(table.columnCount()):
        table.item(rowIndex, 3).setBackground(color)
        table.item(rowIndex, 3).setTextAlignment(Qt.AlignCenter)

    def set_color_to_row_inside(self, table, rowIndex, color):
        # for j in range(table.columnCount()):
        table.item(rowIndex, 2).setBackground(color)
        table.item(rowIndex, 2).setTextAlignment(Qt.AlignCenter)

    # method for showing cars entry
    def update_entry(self):
        for i in reversed(range(self.ui.cars_entry_table.rowCount())):
            self.ui.cars_entry_table.removeRow(i)
        header = self.ui.cars_entry_table.horizontalHeader()
        header.setStretchLastSection(True)
        self.ui.cars_entry_table.setFont(QFont("Arial", 12))
        self.ui.cars_entry_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tableHeaders = ["Maşynyň Nomeri", "Maşynyň Kysymy", "Wagty", "Hereketiň Ugry"]
        self.ui.cars_entry_table.setColumnCount(4)
        for i in range(len(tableHeaders)):
            self.ui.cars_entry_table.setHorizontalHeaderItem(
                i, QTableWidgetItem(tableHeaders[i]))
            self.ui.cars_entry_table.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.ResizeToContents)

        movements = handle_get_requests(enter_url)
        print("Inside: ", len(movements))
        # print("Movements: ", movements)
        for c in movements:
            # print("c object: ", c)
            rowNumber = self.ui.cars_entry_table.rowCount()
            self.ui.cars_entry_table.insertRow(rowNumber)
            # car = handle_get_requests(c["car"]["url"])
            # print("Car obj: ", car)
            for colNumber in range(len(c)):
                if colNumber == 0:
                    data = c["car"]['license_number']
                elif colNumber == 1:
                    data = c["car"]['model_car']
                elif colNumber == 2:
                    data = self.parse_date(c["time"])
                self.ui.cars_entry_table.setItem(rowNumber, colNumber, QTableWidgetItem(str(data)))
                if colNumber == 3:
                    data = "Girdi"
                    self.ui.cars_entry_table.setItem(rowNumber, colNumber, QTableWidgetItem(str(data)))
            self.set_color_to_row_entry(self.ui.cars_entry_table, rowNumber, QColor("Green"))

    # method for showing cars entry
    def update_exit(self):
        for i in reversed(range(self.ui.cars_exit_table.rowCount())):
            self.ui.cars_exit_table.removeRow(i)
        header = self.ui.cars_exit_table.horizontalHeader()
        header.setStretchLastSection(True)
        self.ui.cars_exit_table.setFont(QFont("Arial", 12))

        self.ui.cars_exit_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tableHeaders = ["Maşynyň Nomeri", "Maşynyň Kysymy", "Wagty", "Hereketiň Ugry"]
        self.ui.cars_exit_table.setColumnCount(4)
        for i in range(len(tableHeaders)):
            self.ui.cars_exit_table.setHorizontalHeaderItem(
                i, QTableWidgetItem(tableHeaders[i]))
            self.ui.cars_exit_table.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.ResizeToContents)

        movements = handle_get_requests(exit_url)
        print("Outside: ", len(movements))

        for c in movements:
            rowNumber = self.ui.cars_exit_table.rowCount()
            self.ui.cars_exit_table.insertRow(rowNumber)
            # car = handle_get_requests(c["car"]["url"])
            for colNumber in range(len(c)):
                if colNumber == 0:
                    data = c["car"]['license_number']
                elif colNumber == 1:
                    data = c["car"]['model_car']
                elif colNumber == 2:
                    data = self.parse_date(c["time"])
                self.ui.cars_exit_table.setItem(rowNumber, colNumber, QTableWidgetItem(str(data)))
                if colNumber == 3:
                    data = "Çykdy"
                    self.ui.cars_exit_table.setItem(rowNumber, colNumber, QTableWidgetItem(str(data)))
            self.set_color_to_row_entry(self.ui.cars_exit_table, rowNumber, QColor("RED"))

    # method for showing cars inside/outside
    def update_inside(self, dlg, cars):
        for i in reversed(range(dlg.inside_cars.rowCount())):
            dlg.inside_cars.removeRow(i)
        header = dlg.inside_cars.horizontalHeader()
        header.setStretchLastSection(True)
        dlg.inside_cars.setFont(QFont("Arial", 12))
        dlg.inside_cars.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tableHeaders = ["Maşynyň Nomeri", "Maşynyň Kysymy", "Nirdeligi"]
        dlg.inside_cars.setColumnCount(3)
        for i in range(len(tableHeaders)):
            dlg.inside_cars.setHorizontalHeaderItem(
                i, QTableWidgetItem(tableHeaders[i]))
            dlg.inside_cars.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.ResizeToContents)

        movements = []
        for car in cars:
            if car['movement'] == 'Girdi':
                movements.append(car)
        # print("Inside: ", len(movements))
        print("Movements: ", movements)
        for c in movements:
            # print("c object: ", c)
            rowNumber = dlg.inside_cars.rowCount()
            dlg.inside_cars.insertRow(rowNumber)
            # car = handle_get_requests(c["car"]["url"])

            for colNumber in range(3):
                if colNumber == 0:
                    data = c['license_number']
                    dlg.inside_cars.setItem(rowNumber, colNumber, QTableWidgetItem(str(data)))
                elif colNumber == 1:
                    data = c['model_car']
                    dlg.inside_cars.setItem(rowNumber, colNumber, QTableWidgetItem(str(data)))
                if colNumber == 2:
                    data = "Içinde"
                    dlg.inside_cars.setItem(rowNumber, colNumber, QTableWidgetItem(str(data)))
            self.set_color_to_row_inside(dlg.inside_cars, rowNumber, QColor("Green"))

    # method for showing cars entry
    def update_outside(self, dlg, cars):
        for i in reversed(range(dlg.outside_cars.rowCount())):
            dlg.outside_cars.removeRow(i)
        header = dlg.outside_cars.horizontalHeader()
        header.setStretchLastSection(True)
        dlg.outside_cars.setFont(QFont("Arial", 12))

        dlg.outside_cars.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tableHeaders = ["Maşynyň Nomeri", "Maşynyň Kysymy", "Hereketiň Ugry"]
        dlg.outside_cars.setColumnCount(3)
        for i in range(len(tableHeaders)):
            dlg.outside_cars.setHorizontalHeaderItem(
                i, QTableWidgetItem(tableHeaders[i]))
            dlg.outside_cars.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.ResizeToContents)

        movements = []
        for car in cars:
            if car['movement'] == 'Çykdy':
                movements.append(car)
        print(movements)
        # movements = handle_get_requests(exit_url)
        # print("Outside: ", len(movements))

        for c in movements:
            rowNumber = dlg.outside_cars.rowCount()
            dlg.outside_cars.insertRow(rowNumber)
            # car = handle_get_requests(c["car"]["url"])
            for colNumber in range(3):
                if colNumber == 0:
                    data = c['license_number']
                    dlg.outside_cars.setItem(rowNumber, colNumber, QTableWidgetItem(str(data)))
                elif colNumber == 1:
                    data = c['model_car']
                    dlg.outside_cars.setItem(rowNumber, colNumber, QTableWidgetItem(str(data)))
                if colNumber == 2:
                    data = "Daşynda"
                    dlg.outside_cars.setItem(rowNumber, colNumber, QTableWidgetItem(str(data)))
            self.set_color_to_row_inside(dlg.outside_cars, rowNumber, QColor("RED"))

def main():
    app = QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()