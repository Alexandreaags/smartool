import os
import pyqtgraph as pg
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QMainWindow)

class MainWindow(QMainWindow):
    def __init__(self, experiment=None):
        super().__init__()

        self.scan_data_mag = []
        self.scan_range_mag = []

        base_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(base_dir, 'GUI', 'main_window.ui')
        uic.loadUi(ui_file, self)

        self.experiment = experiment        

        self.step_line.setText(str(self.experiment.config['Scan'] ['num_steps']))
        self.delay_line.setText(self.experiment.config['Scan']['delay'])
        self.sensor_name_box.addItems(self.experiment.sensor)

        self.plot_widget = pg.PlotWidget()
        self.plot = self.plot_widget.plot([0],[0])
        layout = self.central_widget.layout()
        layout.addWidget(self.plot_widget)
        
        # Set labels for X axis
        self.plot_widget.setLabel('bottom', text='Samples')

        self.start_button.clicked.connect(self.start_scan)
        self.stop_button.clicked.connect(self.stop_scan)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)

        self.timer.timeout.connect(self.update_gui)
         
    def start_scan(self):
        num_steps = int(self.step_line.text())
        delay = self.delay_line.text()

        self.experiment.config['Scan'].update(
            {
            'num_steps': num_steps,
            'delay': delay,
            })
        self.experiment.data_title = self.sensor_name_box.currentText()
        self.experiment.start_scan(self.sensor_name_box.currentText())
        print('Scan Started')

    def stop_scan(self):
        self.experiment.stop_scan()
        print('Scan Stopped')
        self.experiment.save_data()
        print('Data Saved')

    def update_plot(self):
        if self.experiment.is_running == True:
            self.scan_data_mag = []
            self.scan_range_mag = []
            for i in self.experiment.array_index_plot:
                self.scan_data_mag.append(self.experiment.scan_data[i].m_as(self.experiment.data_unit))
                self.scan_range_mag.append(self.experiment.scan_range[i])

            self.plot.setData(self.scan_range_mag, 
                            self.scan_data_mag)
            # Set label for Y axis
            self.plot_widget.setLabel('left', text=self.experiment.data_unit_label)
        
    def update_gui(self):
        if self.experiment.is_running:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)