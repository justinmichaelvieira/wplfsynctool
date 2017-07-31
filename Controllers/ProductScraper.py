# ProductScraper.py2
# Justin Vieira 3/18/16

# Imports
from bs4 import BeautifulSoup
import sys
import requests
import traceback

# Class Definition
class ProductScraper:
    def __init__(self, config):
        self.url = config['leafly_url']
        self.debug = True
        self.allProductInfo = [] # This is a list of the following form: [ Name, [List of Weights or Counts], [List of Prices] ] 
        self.productNameDict = {}
        
    # Defines a AllProductInfoList "property" for use by other classes
    def set_allProductInfo(self, value):
        self.allProductInfo = value
    def get_allProductInfo(self):
        return self.allProductInfo
    AllProductInfoList = property(get_allProductInfo, set_allProductInfo)
    
    # Defines a ProductNameDict "property" for use by other classes
    def set_productNameDict(self, value):
        self.productNameDict = value
    def get_productNameDict(self):
        return self.productNameDict
    ProductNameDict = property(get_productNameDict, set_productNameDict)
    
    #Fills local cache / containers with product data
    def processPage(self,  line):
        #do some scrapy stuff with url responses
        try:
            response = requests.get(line)
            html = response.text
            soup = BeautifulSoup(html,  "html.parser")
            #Get all the tags we need here
            products = soup.findAll("div", class_="item-heading--body")
            #Filter out tags so we just have text results
            for currentProduct in products:
                currentPrices = currentProduct.findAll("span", class_="colored")
                tempPriceList = []
                for price in currentPrices:
                    for pricestring in price.stripped_strings:
                        tempPriceList.append(str(pricestring))
                currentPriceHeadings = currentProduct.findAll("span", class_="copy--upper")
                tempPriceHeadings = []
                i = 1
                for heading in currentPriceHeadings:
                    for headingstring in heading.stripped_strings:
                        if i % 2 == 0:
                            tempPriceHeadings.append(str(headingstring))
                        i = i+1
                        
                #Store the single product info in the class' various containers 
                tempProductName = currentProduct.attrs['title']
                tempProductInfo = [ tempProductName, tempPriceList, tempPriceHeadings]
                self.allProductInfo.append(tempProductInfo)
                self.productNameDict[tempProductName] = tempProductInfo
                
            if self.debug:
                print(self.allProductInfo)
        except:
            for tb in traceback.format_tb(sys.exc_info()[2]):
                print(tb)

    def scrapeProductData(self):
        self.processPage(self.url)
        
    def productIsInCache(self, productName):
        if productName in self.productNameDict:
            return True
        return False
