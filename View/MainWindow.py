import yaml
from PyQt5.QtWidgets import *
from pprint import pprint, pformat

from View.mainwindow_auto import Ui_MainWindow


class MainWindow(QDialog, Ui_MainWindow):
    def __init__(self, config, scraper, api):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self._config = config
        self._scraper = scraper
        self._wcController = api
        self.pushButton.clicked.connect(self.performSync)
        self.editSettingsBtn.clicked.connect(self.editContent)
        self.saveSettingsBtn.clicked.connect(self.saveContent)
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
        self.saveSettingsBtn.setDisabled(editable)
        self.editSettingsBtn.setDisabled(not editable)

    def setUiFromConfig(self):
        self.wmPageEdit.setText(self._config['leafly_url'])
        self.wpApiUrlEdit.setText(self._config['wp_url'])
        self.consKeyEdit.setText(self._config['consumer_key'])
        self.secretKeyEdit.setText(self._config['consumer_secret'])

    def performSync(self):
        if(self._wcController._wcapi == None):
            self._wcController.initWcapi()
        leaflyProducts = self._scraper.scrapeProductData()
        wcProducts = self._wcController.getAllProducts().json()
        pprint(wcProducts)
        #self.onOutputChanged(pformat(wcProducts))
        self._wcController.deleteProducts(wcProducts)
        for prodName in leaflyProducts:
            prodInfo = leaflyProducts[prodName]
            # create if not exists, otherwise update
            self._wcController.createVariableProduct(prodName, prodInfo)

    def setCentralWidget(self, nullArg):
        pass

    def onOutputChanged(self, allProducts):
        self.outputText.appendPlainText(allProducts)
