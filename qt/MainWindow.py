from PyQt5.QtWidgets import *
#import numpy as np
from qt.mainwindow_auto import Ui_MainWindow

class MainWindow(QDialog, Ui_MainWindow):

    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self._config = config
        self.pushButton_2.clicked.connect(self.editContent)
        self.pushButton_3.clicked.connect(self.saveContent)
        self.setUiFromConfig()
        self.setDisabled(True)

    def closeDialog(self):
        self.close()

    def editContent(self):
        self.setDisabled(False)

    def saveContent(self):
        self.setDisabled(True)

    def setDisabled(self, editable):
        self.wmPageEdit.setDisabled(editable)
        self.wpApiUrlEdit.setDisabled(editable)
        self.consKeyEdit.setDisabled(editable)
        self.secretKeyEdit.setDisabled(editable)

    def setUiFromConfig(self):
        self.wmPageEdit.setText(self._config['leafly_url'])
        self.wpApiUrlEdit.setText(self._config['wp_url'])
        self.consKeyEdit.setText(self._config['consumer_key'])
        self.secretKeyEdit.setText(self._config['consumer_secret'])