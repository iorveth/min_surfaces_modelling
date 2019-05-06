import sys
import plotly.offline as py
import plotly.graph_objs as go
from characteristic_quadrilateral import СharacteristicQuadrilateral
from ui.dialog_characteristic_quadrilateral import *
from ui.dialog_k import *
from ui.main_window import *

class DialogСharacteristicQuadrilateral(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent
        self.ui = Ui_DialogСharacteristicQuadrilateral()
        self.ui.setupUi(self)
        self.all_line_edits = [self.ui.lineEdit, self.ui.lineEdit_2, self.ui.lineEdit_3, self.ui.lineEdit_4,
            self.ui.lineEdit_5, self.ui.lineEdit_6, self.ui.lineEdit_7, self.ui.lineEdit_8, self.ui.lineEdit_9, 
                self.ui.lineEdit_10, self.ui.lineEdit_11, self.ui.lineEdit_12]
        self.characteristic_quadrilateral_coordinates = [None] * 12
        self.ui.buttonBox.accepted.connect(self.process_input)

    def catch_not_complex_number_error(self, value):
        try:
            number = complex(value)
            return number
        except Exception:
            QtWidgets.QMessageBox(self).about(self, 'Error','Input can only be a number/complex number')

    def process_input(self):
        for i in range(len(self.all_line_edits)):
            if self.all_line_edits[i].isEnabled():
                self.characteristic_quadrilateral_coordinates[i] = self.catch_not_complex_number_error(self.all_line_edits[i].text())
                if self.characteristic_quadrilateral_coordinates[i]:
                    self.all_line_edits[i].setEnabled(False)

        if all(elem is not None for elem in self.characteristic_quadrilateral_coordinates):
            self.parent.quadrilateral = СharacteristicQuadrilateral(self.characteristic_quadrilateral_coordinates)
            if not self.parent.ui.pushButton_3.isEnabled():
                self.parent.ui.pushButton_3.setEnabled(True)
                self.parent.ui.pushButton_4.setEnabled(True)
            self.close()

class DialogK(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent
        self.ui = Ui_DialogK()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.process_input)

    def catch_not_number_error(self, value):
        try:
            number = float(value)
            return number
        except Exception:
            QtWidgets.QMessageBox(self).about(self, 'Error','Input can only be a number')

    def process_input(self):
        self.parent.k = self.catch_not_number_error(self.ui.lineEdit.text())
        if self.parent.k:
            self.parent.current_fig = self.parent.quadrilateral.create_minimal_surface_quasiconformal_replacement("Minimal Surface, based on characteristic quadrilateral with quasiconformal parameter replacement", self.parent.k)
            self.parent.fig_list.append(self.parent.current_fig)
            if not self.parent.ui.pushButton_2.isEnabled(): self.parent.ui.pushButton_2.setEnabled(True)
            if (not self.parent.ui.pushButton.isEnabled()) and (len(self.parent.fig_list) > 1): self.parent.ui.pushButton.setEnabled(True)
            self.close()

class MainWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_fig = None
        self.fig_list = []
        self.ui.pushButton2.clicked.connect(self.open_characteristic_quadrilateral_dialog)
        self.ui.pushButton_3.clicked.connect(self.open_create_minimal_surface_quasiconformal_replacement_dialog)
        self.ui.pushButton_4.clicked.connect(self.create_minimal_surface_conformal_replacement)
        self.ui.pushButton_2.clicked.connect(self.plot)
        self.ui.pushButton.clicked.connect(self.plot_all)

    def open_characteristic_quadrilateral_dialog(self):
        dialog = DialogСharacteristicQuadrilateral(self)
        dialog.show()

    def open_create_minimal_surface_quasiconformal_replacement_dialog(self):
        dialog = DialogK(self)
        dialog.show()

    def create_minimal_surface_conformal_replacement(self):
        self.current_fig = self.quadrilateral.create_minimal_surface_conformal_replacement("Minimal Surface, based on characteristic quadrilateral with conformal parameter replacement")
        self.fig_list.append(self.current_fig)
        if not self.ui.pushButton_2.isEnabled(): self.ui.pushButton_2.setEnabled(True)
        if (not self.ui.pushButton.isEnabled()) and (len(self.fig_list) > 1): self.ui.pushButton.setEnabled(True)

    def plot(self):
        py.plot(self.current_fig, "Minimal Surface, based on characteristic quadrilateral")

    def plot_all(self):
        data = []
        data_layout = []
        for fig in self.fig_list:
            data.append(fig.data[0])
            data_layout.append(fig.data[1])
        data += data_layout
        fig = go.Figure(data=data)
        py.plot(fig, "Minimal Surface, based on characteristic quadrilateral")

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWin()
    myapp.show()
    sys.exit(app.exec_())