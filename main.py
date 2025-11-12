# crate a gui that finds the correct resistor or capacitor
from datetime import datetime

from PyQt6.QtWidgets import QWidget, QMainWindow

from utils.db import JLCPCBDatabase, COLUMNS, ValueInvalid, PackageInvalid

# import libraries
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal

from create_symbol import createResistorSymbol, createCapacitorSymbolSmall, createCapacitorSymbol, createResistorSymbolSmall

import sys

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QtWidgets.QApplication(sys.argv)


class DatabaseUpdateWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, db):
        super().__init__()
        self.db = db

    def run(self):
        try:
            self.db.update()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Component Finder")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QtWidgets.QGridLayout(self.centralWidget)
        self.setLayout(self.layout)
        self.dataBaseStatus = QtWidgets.QLabel("- Database Status -")
        self.layout.addWidget(self.dataBaseStatus, 0, 1, 1, 3)
        self.updateBtn = QtWidgets.QPushButton("Update Database")
        self.layout.addWidget(self.updateBtn, 0, 0)
        self.radio_buttons = QtWidgets.QButtonGroup()
        self.radio_buttons.setExclusive(True)
        self.radio1 = QtWidgets.QRadioButton("Capacitor")
        self.layout.addWidget(self.radio1, 1, 0)
        self.radio2 = QtWidgets.QRadioButton("Resistor")
        self.layout.addWidget(self.radio2, 1, 1)
        self.radio_buttons.addButton(self.radio1)
        self.radio_buttons.addButton(self.radio2)
        self.small_check = QtWidgets.QCheckBox("Small footprints")
        self.small_check.setChecked(True)
        self.layout.addWidget(self.small_check, 1, 3)
        self.layout.addWidget(QtWidgets.QLabel("Value"), 2, 0)
        self.value_input = QtWidgets.QLineEdit()
        self.layout.addWidget(self.value_input, 2, 1)
        self.layout.addWidget(QtWidgets.QLabel("Package"), 2, 2)
        self.package_input = QtWidgets.QLineEdit()
        self.layout.addWidget(self.package_input, 2, 3)


        self.output_table = QtWidgets.QTableWidget()
        self.output_table.setColumnCount(len(COLUMNS))
        self.output_table.setHorizontalHeaderLabels(COLUMNS)
        self.output_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        #self.output_table.setSortingEnabled(True)
        self.layout.addWidget(self.output_table, 3, 0, 1, 4)

        self.db = JLCPCBDatabase("cache.sqlite3")

        self.radio_buttons.buttonClicked.connect(self.update_table)
        self.value_input.textChanged.connect(self.update_table)
        self.package_input.textChanged.connect(self.update_table)
        self.output_table.cellDoubleClicked.connect(self.createSymbol)
        self.updateBtn.clicked.connect(self.updateDatabase)

        self.radio1.setChecked(True)
        if self.db.status():
            self.updateDatabaseStatus()
            self.db.open()
        self.update_table()

    def updateDatabase(self):
        self.updateBtn.setEnabled(False)
        self.dataBaseStatus.setText("Updating database...")
        self.worker = DatabaseUpdateWorker(self.db)
        self.worker.finished.connect(self.onUpdateFinished)
        self.worker.error.connect(self.onUpdateError)
        self.worker.start()

    def onUpdateFinished(self):
        self.updateBtn.setEnabled(True)
        self.update_table()
        self.updateDatabaseStatus()

    def onUpdateError(self, error_msg):
        self.updateBtn.setEnabled(True)
        self.dataBaseStatus.setText(f"Update failed: {error_msg}")

    def updateDatabaseStatus(self):
        status = self.db.status()
        if status:
            self.dataBaseStatus.setText("Database last updated on: " + str(datetime.fromtimestamp(status)))
        else:
            self.dataBaseStatus.setText("Database not found")
    def update_table(self):
        if not self.db.status():
            return
        is_capacitor = self.radio1.isChecked()
        if is_capacitor:
            try:
                results = self.db.get_capacitors(self.value_input.text(), self.package_input.text())
            except ValueInvalid:
                self.value_input.setStyleSheet("background-color: red")
                return
            except PackageInvalid:
                self.package_input.setStyleSheet("background-color: red")
                return
        else:
            try:
                results = self.db.get_resistors(self.value_input.text(), self.package_input.text())
            except ValueInvalid:
                self.value_input.setStyleSheet("background-color: red")
                return
            except PackageInvalid:
                self.package_input.setStyleSheet("background-color: red")
                return
        self.value_input.setStyleSheet("")
        self.package_input.setStyleSheet("")

        # Hide voltage column for resistors, show for capacitors
        voltage_col_index = COLUMNS.index("voltage")
        self.output_table.setColumnHidden(voltage_col_index, not is_capacitor)

        self.output_table.setRowCount(len(results))
        for i, row_dict in enumerate(results):
            for j, col_name in enumerate(COLUMNS):
                value = row_dict.get(col_name, "")
                self.output_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        self.output_table.resizeColumnsToContents()
        self.output_table.resizeRowsToContents()

    def createSymbol(self):
        row = self.output_table.currentRow()
        value = self.output_table.item(row, COLUMNS.index("value")).text()
        package = self.output_table.item(row, COLUMNS.index("package")).text()
        lcsc = self.output_table.item(row, COLUMNS.index("lcsc")).text()
        voltage = self.output_table.item(row, COLUMNS.index("voltage")).text()
        use_small_symbol = self.small_check.isChecked()
        if self.radio1.isChecked():
            symbol = createCapacitorSymbolSmall(value, package, lcsc, voltage) if use_small_symbol else createCapacitorSymbol(value, package, lcsc, voltage)
        else:
            symbol = createResistorSymbolSmall(value, package, lcsc) if use_small_symbol else createResistorSymbol(value, package, lcsc)
        # add symbol to clipboard
        clipboard = QtGui.QGuiApplication.clipboard()
        clipboard.setText(symbol)


if __name__ == "__main__":
    # Create a Qt widget, which will be our window.
    window = MainWindow()
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec()
