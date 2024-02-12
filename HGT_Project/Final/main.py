from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from pyqtgraph import PlotWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from gui import Ui_Form
from controller import Controller
import threading

if __name__ == "__main__":
    try:
        # Creating the application
        app = QApplication([])

        # Set the application style to Fusion
        app.setStyle('Fusion')

        # Set a dark palette for the application
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(dark_palette)

        # If using a raspberry pi
        piMode = True
        setHX711 = True

        # Create instances of the GUI, JSON_Server, and Controller
        gui = Ui_Form()
        controller = Controller(gui , piMode, setHX711)

        # Creating a timer that will constantly loop the following methods
        timer = QTimer()

        # Updating the measured weight
        timer.timeout.connect(controller.updateWeight)

        # Updating the schedule
        timer.timeout.connect(controller.updateSchedule)

        # The controller will actuate according to the measured weight
        timer.timeout.connect(controller.controls)

        # Save the file locally and upload to github
        # timer.timeout.connect(controller.save_data)

        # Plot the readings
        timer.timeout.connect(controller.plot_chart)

        # Repeat the timer every 0.1 seconds
        timer.start(100)

        # Showing the window
        controller.main_win.show()
        app.exec_()
    

    except:
        controller.file_path.close()
        controller.file_backup_path.close()
        sys.exit(app.exec_())
