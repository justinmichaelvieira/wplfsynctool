from PyQt5.QtWidgets import *
#import numpy as np
from qt.mainwindow_auto import Ui_MainWindow
import yaml

class MainWindow(QDialog, Ui_MainWindow):

    def __init__(self, config, scraper, api):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self._config = config
        self._scraper = scraper
        self._api = api
        self.pushButton.clicked.connect(self.performSync)
        self.pushButton_2.clicked.connect(self.editContent)
        self.pushButton_3.clicked.connect(self.saveContent)
        self.setUiFromConfig()
        self.setDisabled(True)

    def closeDialog(self):
        self.close()

    def editContent(self):
        self.setDisabled(False)

    def saveContent(self):
        stream = open('config.yml', 'w')
        self._config['leafly_url'] = self.wmPageEdit.text()
        self._config['wp_url'] = self.wpApiUrlEdit.text()
        self._config['consumer_key'] = self.consKeyEdit.text()
        self._config['consumer_secret'] = self.secretKeyEdit.text()
        yaml.dump(self._config, stream)
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

    def performSync(self):
        if(self._api.wcapi == None):
            self._api.initWcapi()
        self._scraper.scrapeProductData()
        self._api.printAllProducts()

    def setCentralWidget(self, nullArg):
        pass