import json
import requests
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QGridLayout, QLabel, QLineEdit,
    QPlainTextEdit, QPushButton, QWidget
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.reset_widgets()

    def init_ui(self):
        self.setWindowTitle("Simple API Tester")

        lbEndpoint = QLabel("Endpoint:")
        self.leEndPoint = QLineEdit(text="http://localhost:5000/values")
        
        lbMethod = QLabel("Method:")
        self.cmbMethod = QComboBox()
        self.cmbMethod.addItems(['GET', 'POST', 'DELETE'])
        self.cmbMethod.currentTextChanged.connect(self.reset_widgets)

        self.chbPrefix = QCheckBox("?prefix=")
        self.lePrefix = QLineEdit()

        self.lbKey = QLabel("key:")
        self.leKey = QLineEdit()
        self.lbValue = QLabel("value:")
        self.leValue = QLineEdit()

        self.btSend = QPushButton(text="Send request")
        self.btSend.clicked.connect(self.sendRequest)

        lbHeader = QLabel("Status + Headers:")
        self.teHeader = QPlainTextEdit()
        lbResponse = QLabel("Body:")
        self.teResponse = QPlainTextEdit()

        grid = QGridLayout()
        grid.setSpacing(4)

        grid.addWidget(lbEndpoint, 0, 0)
        grid.addWidget(self.leEndPoint, 0, 1, 1, 3)
        grid.addWidget(lbMethod, 1, 0)
        grid.addWidget(self.cmbMethod, 1, 1, 1, 3)
        grid.addWidget(self.chbPrefix, 2, 0)
        grid.addWidget(self.lePrefix, 2, 1, 1, 3)
        grid.addWidget(self.lbKey, 3, 0)
        grid.addWidget(self.leKey, 3, 1)
        grid.addWidget(self.lbValue, 3, 2)
        grid.addWidget(self.leValue, 3, 3)
        grid.addWidget(self.btSend, 4, 0, 1, 4, Qt.AlignRight)
        grid.addWidget(lbHeader, 5, 0, 1, 4)
        grid.addWidget(self.teHeader, 6, 0, 1, 4)
        grid.addWidget(lbResponse, 7, 0, 1, 4)
        grid.addWidget(self.teResponse, 8, 0, 1, 4)

        self.setLayout(grid)
        self.show()

    def reset_widgets(self):
        value = self.cmbMethod.currentText()

        self.chbPrefix.setEnabled(value == 'GET')
        self.lePrefix.setEnabled(value == 'GET')

        self.lbKey.setEnabled(value == 'POST')
        self.leKey.setEnabled(value == 'POST')
        self.lbValue.setEnabled(value == 'POST')
        self.leValue.setEnabled(value == 'POST')

        self.leEndPoint.setText("http://localhost:5000/values")
        self.chbPrefix.setChecked(False)
        self.lePrefix.setText("")
        self.leKey.setText("")
        self.leValue.setText("")

    def sendRequest(self):
        url = self.leEndPoint.text()
        method = self.cmbMethod.currentText()

        try:
            if method == 'GET':
                prefix = ""
                params = {}
                if self.chbPrefix.isChecked():
                    prefix = self.lePrefix.text()
                    params = {'prefix': prefix}

                if params:
                    response = requests.get(url, params=params)
                else:
                    response = requests.get(url)

            elif method == 'POST':
                key = self.leKey.text()
                value = self.leValue.text()
                
                response = requests.post(url, json={'key': key, 'value': value})
            else:  # method == 'DELETE'
                response = requests.delete(url)
        except requests.exceptions.ConnectionError as e:
            headers = []
            response_msg = 'Failed to establish a new connection: [Errno 111] Connection refused\nMake sure that server is running...'
        else:  # No exception occured
            version_str = 'HTTP/1.1' if response.raw.version == 11 else 'HTTP/1.0'
            headers = []
            for k, v in response.headers.items():
                headers.append(": ".join([k, v]))
            try:
                response_msg = json.dumps(response.json(), indent=4)
            except ValueError:
                response_msg = ""
            status_line = " ".join([version_str, str(response.status_code), response.reason, "\n"]) 
            headers.insert(0, status_line)

        self.teHeader.setPlainText("\n".join(headers))
        self.teResponse.setPlainText(response_msg)    


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
