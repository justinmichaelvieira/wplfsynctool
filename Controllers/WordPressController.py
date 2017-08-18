from woocommerce import API
from pprint import pprint, pformat

# Class Definition
class WordPressController:
    def __init__(self, config):
        self._config = config
        self._wcapi = None

    def initWcapi(self):
        self._wcapi = API(
            url=self._config['wp_url'],
            consumer_key=self._config['consumer_key'],
            consumer_secret=self._config['consumer_secret'],
            wp_api=True,
            query_string_auth=True,
            version="wc/v1"
        )
            
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
    ProductNameIdDict = property(get_productNameDict, set_productNameDict)

    # Creation functions
    
    def createSimpleProduct(self, name, price):
        data = {
            "name": name, "type": "simple", "regular_price": price, "description": name, "short_description": name,
        }
        pprint(self._wcapi.post("products", data).json())
        
    def createVariableProduct(self, name, prodInfo):
        variations = []
        options = []

        for x in range(len(prodInfo[0])):
            variations.append({"regular_price": prodInfo[0][x], "attributes": [{"name": "Size","option": prodInfo[1][x]}]})
            options.append(prodInfo[1][x])

        data = {
        "name": name, "type": "variable", "description": name, "short_description": name,
        "attributes": [
            {
                "position": 0, "visible": True, "variation": True,
                "options": options
            }
        ],
        "default_attributes": [
            {
                "name": "Size",
                "option": options[0]
            }
        ],
        "variations": variations
        }
        self._wcapi.post("products", data)

    # Read functions
    
    #Reads product list stored in WP site and populates local product info cache containers
    def populateProducts(self):
        self.set_allProductInfo(self._wcapi.get("products"))
        
        for pInfo in self.AllProductInfoList:
                self.ProductNameIdDict[pInfo.name] = pInfo.id
                
        return self.get_allProductInfo()
        
    def printAllProducts(self):
        productsJson = self._wcapi.get("products").json()
        pprint(productsJson)
        return pformat(productsJson)

    def getAllProducts(self):
        return self._wcapi.get("products")
        
    def getProductIdByName(self):
        pass
        
    # Update functions
    
    def updateProduct(self, productId, price, name, catId = "", category = "", catslug = ""):
        data = {
            "regular_price": price,
            "name" : name,
            "categories": [
                { "id": catId, "name": category, "slug": catslug }]
        }
        pprint(self._wcapi.put(''.join(["products/", productId], data).json()))
    
    # Delete functions
    
    def deleteProduct(self, productId):
        out = self._wcapi.delete(''.join(["products/" , productId , "?force=true"]))
        return out.ok
        
    def deleteProducts(self, productList):
        out = "Deleting products.\n"

        for product in productList:
            pid = str(product['id'])
            if self.deleteProduct(pid):
                out += pid + " deleted.\n"
            else:
                out += "warning: error deleting " + pid + ".\n"

        return out
