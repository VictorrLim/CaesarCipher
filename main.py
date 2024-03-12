import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QRadioButton, QCheckBox, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont

class CaesarCipher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Caesar Cipher')
        self.setGeometry(100, 100, 400, 700)

        font = QFont('Arial', 12)

        label_text = QLabel('Text:', self)
        label_text.setFont(font)
        label_text.move(20, 20)

        self.input_text = QLineEdit(self)
        self.input_text.setFont(font)
        self.input_text.move(20, 50)
        self.input_text.resize(360, 30)

        label_shift = QLabel('Shift:', self)
        label_shift.setFont(font)
        label_shift.move(20, 100)

        self.input_shift = QLineEdit(self)
        self.input_shift.setFont(font)
        self.input_shift.move(80, 100)
        self.input_shift.resize(50, 30)

        self.radio_encrypt = QRadioButton('Encrypt', self)
        self.radio_encrypt.setFont(font)
        self.radio_encrypt.move(150, 100)
        self.radio_encrypt.setChecked(True)

        self.radio_decrypt = QRadioButton('Decrypt', self)
        self.radio_decrypt.setFont(font)
        self.radio_decrypt.move(250, 100)

        self.checkbox_save = QCheckBox('Save output to file', self)
        self.checkbox_save.setFont(font)
        self.checkbox_save.move(40, 150)

        button_load = QPushButton('Load from file', self)
        button_load.setFont(font)
        button_load.move(200, 150)
        button_load.clicked.connect(self.load_from_file)

        button_process = QPushButton('Process', self)
        button_process.setFont(font)
        button_process.move(150, 200)
        button_process.clicked.connect(self.process_text)

        self.output_text = QTextEdit(self)
        self.output_text.setFont(font)
        self.output_text.move(20, 240)
        self.output_text.resize(360, 200)

    def load_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Load from file', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
                self.input_text.setText(text)

    def process_text(self):
        text = self.input_text.text()
        shift = self.input_shift.text()

        if not text:
            QMessageBox.warning(self, 'Error', 'Please enter some text.')
            return

        if not shift or not shift.isdigit():
            QMessageBox.warning(self, 'Error', 'Please enter a valid shift value.')
            return

        shift = int(shift)

        if self.radio_encrypt.isChecked():
            result = self.encrypt(text, shift)
        else:
            result = self.decrypt(text, shift)

        self.output_text.setPlainText(result)

        if self.checkbox_save.isChecked():
            self.save_to_file(result)

    def encrypt(self, text, shift):
        result = ''
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result

    def decrypt(self, text, shift):
        result = ''
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            else:
                result += char
        return result

    def save_to_file(self, text):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save to file', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'w') as file:
                file.write(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    cipher = CaesarCipher()
    cipher.show()
    sys.exit(app.exec_())