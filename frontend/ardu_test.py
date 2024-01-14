import sys

from PyQt5 import QtCore, QtWidgets, QtSerialPort
from PyQt5.QtWidgets import QApplication, QMainWindow ,QWidget ,QToolBar, \
    QHBoxLayout, QAction ,QStatusBar ,QLineEdit ,QPushButton ,QTextEdit , QVBoxLayout
from PyQt5.QtCore import Qt , pyqtSignal
from PyQt5.QtSerialPort import QSerialPortInfo

class AddComport(QMainWindow):
    porttnavn = pyqtSignal(str)

    def __init__(self, parent , menu):
        super().__init__(parent)


        menuComporte = menu.addMenu("Comporte")

        info_list = QSerialPortInfo()
        serial_list = info_list.availablePorts()
        serial_ports = [port.portName() for port in serial_list]
        if(len(serial_ports)> 0):
            antalporte = len(serial_ports)
            antal = 0
            while antal < antalporte:
                button_action = QAction(serial_ports[antal], self)
                txt = serial_ports[antal]
                portinfo = QSerialPortInfo(txt)
                buttoninfotxt = " Ingen informationer"
                if portinfo.hasProductIdentifier():
                    buttoninfotxt = ("Produkt specifikation = " + str(portinfo.vendorIdentifier()))
                if portinfo.hasVendorIdentifier():
                    buttoninfotxt =  buttoninfotxt + (" Fremstillers id = "+ str(portinfo.productIdentifier()))
                button_action = QAction( txt , self)
                button_action.setStatusTip( buttoninfotxt)
                button_action.triggered.connect(lambda checked, txt = txt: self.valgAfComportClick(txt))
                menuComporte.addAction(button_action)
                antal = antal +1
        else:
            print("Ingen com porte fundet")

    def valgAfComportClick(self , port):
        self.porttnavn.emit(port)

    def closeEvent(self, event):
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        portname = "None"

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()
        comfinder = AddComport(self , menu)
        comfinder.porttnavn.connect(self.valgAfComport)

        self.setWindowTitle("Serial port display / send")

        self.message_le = QLineEdit()
        self.send_btn = QPushButton(
            text="Send",
            clicked=self.send
        )

        self.output_te = QTextEdit(readOnly=True)
        self.button = QPushButton(
            text="Connect",
            checkable=True,
            toggled=self.on_toggled
        )
        lay = QVBoxLayout(self)
        hlay = QHBoxLayout()
        hlay.addWidget(self.message_le)
        hlay.addWidget(self.send_btn)
        lay.addLayout(hlay)
        lay.addWidget(self.output_te)
        lay.addWidget(self.button)

        widget = QWidget()
        widget.setLayout(lay)
        self.setCentralWidget(widget)

        self.serial = QtSerialPort.QSerialPort(
            portname,
            baudRate=QtSerialPort.QSerialPort.Baud9600,
            readyRead=self.receive)


    @QtCore.pyqtSlot()
    def receive(self):
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            text = text.rstrip('\r\n')
            self.output_te.append(text)

    @QtCore.pyqtSlot()
    def send(self):
        self.serial.write(self.message_le.text().encode())

    @QtCore.pyqtSlot(bool)
    def on_toggled(self, checked):
        self.button.setText("Disconnect" if checked else "Connect")
        if checked:
            if not self.serial.isOpen():
                self.serial.open(QtCore.QIODevice.ReadWrite)
                if not self.serial.isOpen():
                    self.button.setChecked(False)
            else:
                self.button.setChecked(False)
        else:
            self.serial.close()

    def valgAfComport(self , nyport):
        seropen = False
        if self.serial.isOpen():
            seropen = True
            self.serial.close()
        self.serial.setPortName(nyport)
        if seropen:
            self.serial.open(QtCore.QIODevice.ReadWrite)
            if not self.serial.isOpen():
                self.button.setChecked(False)

        print(nyport)

    def closeEvent(self, event):
        self.serial.close()
        print("Comport lukket")
        # print(comporttxt)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())