from PyQt5.QtWidgets import QApplication

from Smartool.Model.main_model import ArduinoNano
from Smartool.View.main_window import MainWindow

experiment = ArduinoNano('Run\experiment.yml')
# experiment = ArduinoNano('Run\experiment_ale.yml')
experiment.load_config()
experiment.load_daq()

app = QApplication([])
window = MainWindow(experiment)
window.show()
app.exec()

experiment.finalize()