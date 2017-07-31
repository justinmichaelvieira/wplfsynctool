import sys
import yaml
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from Controllers.ProductScraper import ProductScraper
from Controllers.WordPressController import WordPressController
from qt.MainWindow import MainWindow

def main():
    stream = open('config.yml', 'r')
    config = yaml.safe_load(stream)

    p = ProductScraper(config)
    p.scrapeProductData()
    
    w = WordPressController(config)
    wpProductList = w.getAllProducts()

    app = QApplication(sys.argv)
    app.setOrganizationName("Rancorsoft")
    app.setOrganizationDomain("Rancorsoft.com")
    app.setApplicationName("Leafly WPAPI Maps Sync Tool")
    mainWindow = MainWindow(config)
    mainWindow.show()
    # without this, the script exits immediately.
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
