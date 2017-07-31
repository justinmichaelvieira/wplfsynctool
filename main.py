import sys
import PyQt5
from PyQt5 import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

from Controllers.ProductScraper import ProductScraper
from Controllers.WordPressController import WordPressController

def main():
    p = ProductScraper()
    p.scrapeProductData()
    
    w = WordPressController()
    wpProductList = w.getAllProducts()
    
    #for currentProduct in p:
        
    
if __name__ == "__main__":
    main()
