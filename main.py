import os.path as osp
import sys, logging, yaml
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from Controllers.ProductScraper import ProductScraper
from Controllers.WordPressController import WordPressController
from View.MainWindow import MainWindow

def exceptionHook(type, value, tb):
    """ Redirect tracebacks to error log """
    import traceback
    rawreport = traceback.format_exception(type, value, tb)
    report = '\n'.join(rawreport)
    logging.error(report)
    sys.exit()

sys.excepthook = exceptionHook

def main():
    stream = open('config.yml', 'r')
    config = yaml.safe_load(stream)

    p = ProductScraper(config)
    w = WordPressController(config)

    app = QApplication(sys.argv)
    app.setOrganizationName("Rancorsoft")
    app.setOrganizationDomain("Rancorsoft.com")
    app.setApplicationName("Leafly WPAPI Maps Sync Tool")
    mainWindow = MainWindow(config, p, w)
    mainWindow.setWindowIcon(QtGui.QIcon(osp.join(osp.dirname(__file__), 'sync16x16.png')))
    mainWindow.show()
    # without this, the script exits immediately.
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
