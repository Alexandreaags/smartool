import os
import pyqtgraph as pg
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QMainWindow)

class MainWindow(QMainWindow):
    def __init__(self, experiment=None):
        super().__init__()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(base_dir, 'GUI', 'main_window.ui')
        uic.loadUi(ui_file, self)

        self.experiment = experiment        

        self.step_line.setText(str(self.experiment.config['Scan'] ['num_steps']))
        self.delay_line.setText(self.experiment.config['Scan']['delay'])

        self.plot_widget = pg.PlotWidget()
        self.plot = self.plot_widget.plot([0],[0])
        layout = self.central_widget.layout()
        layout.addWidget(self.plot_widget)
        
        self.start_button.clicked.connect(self.start_scan)
        self.stop_button.clicked.connect(self.stop_scan)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)

        #self.actionSave.triggered.connect(self.experiment.save_data)

        self.timer.timeout.connect(self.update_gui)

    def start_scan(self):
        num_steps = int(self.step_line.text())
        delay = self.delay_line.text()

        self.experiment.config['Scan'].update(
            {
            'num_steps': num_steps,
            'delay': delay           
            })
        self.experiment.start_scan()

    def stop_scan(self):
        self.experiment.stop_scan()
        print('Scan Stopped')

    def update_plot(self):
        self.plot.setData(self.experiment.scan_range, 
                          self.experiment.scan_data)
        
    def update_gui(self):
        if self.experiment.is_running:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)