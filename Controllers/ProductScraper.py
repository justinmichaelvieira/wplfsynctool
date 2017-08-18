# ProductScraper.py2
# Justin Vieira 3/18/16

# Imports
from bs4 import BeautifulSoup
import sys
import requests
import traceback
from pprint import pprint

# Class Definition
class ProductScraper:
    def __init__(self, config):
        self._url = config['leafly_url']
        self._debug = True
        self._allProductInfo = {} # self.allProductInfo['name'] = [[List of Weights or Counts], [List of Prices]]

    # Defines allProductInfo property
    def set_allProductInfo(self, value):
        self._allProductInfo = value
    def get_allProductInfo(self):
        return self._allProductInfo
    AllProductInfo = property(get_allProductInfo, set_allProductInfo)
    
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
                tempProductInfo = [tempPriceList, tempPriceHeadings]
                self._allProductInfo[tempProductName] = tempProductInfo

            if self._debug:
                pprint(self._allProductInfo)
        except:
            for tb in traceback.format_tb(sys.exc_info()[2]):
                print(tb)

    def scrapeProductData(self):
        self.processPage(self._url)
        return self._allProductInfo
        
    def productIsInCache(self, productName):
        if productName in self._allProductInfo:
            return True
        return False
