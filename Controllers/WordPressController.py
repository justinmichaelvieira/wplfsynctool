from woocommerce import API

# Class Definition
class WordPressController:
    def __init__(self):
        self.wcapi = API( 
            url="https://leaflywp.justinvieira.com", 
            consumer_key="ck_4d455fd97da0ab14398a52470bca15070eb0c0ac", 
            consumer_secret="cs_07cecb5c54385f86d14a9f80deaaa2ac86f5ca96",
            wp_api=True,
            query_string_auth	=True,
            version="wc/v1"
        )
        self.allProductInfo = self.getAllProducts()
        for currProductInfo in self.allProductInfo:
            self.productNameIdDict[currProductInfo.name] = currProductInfo.id
            
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
            "name": name,
            "type": "simple",
            "regular_price": price,
            "description": name,
            "short_description": name,
            #"categories": [
            #    {
            #        "id": 9
            #    },
            #    {
            #        "id": 14
            #    }
            #],
            #"images": [
            #    {
            #        "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_2_front.jpg",
            #        "position": 0
            #    },
            #    {
            #        "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_2_back.jpg",
            #        "position": 1
            #    }
            #]
        }
        print(self.wcapi.post("products", data).json())
        
    def createVariableProduct(self, name, unitList, priceList):
        data = {
        "name": name,
        "type": "variable",
        "description": name,
        "short_description": name,
        "categories": [
            {
                "id": 9
            },
            {
                "id": 14
            }
        ],
        "images": [
            {
                "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_4_front.jpg",
                "position": 0
            },
            {
                "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_4_back.jpg",
                "position": 1
            },
            {
                "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_3_front.jpg",
                "position": 2
            },
            {
                "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_3_back.jpg",
                "position": 3
            }
        ],
        "attributes": [
            {
                "id": 6,
                "position": 0,
                "visible": False,
                "variation": True,
                "options": [
                    "Black",
                    "Green"
                ]
            },
            {
                "name": "Size",
                "position": 0,
                "visible": True,
                "variation": True,
                "options": [
                    "S",
                    "M"
                ]
            }
        ],
        "default_attributes": [
            {
                "id": 6,
                "option": "Black"
            },
            {
                "name": "Size",
                "option": "S"
            }
        ],
        "variations": [
            {
                "regular_price": "19.99",
                "image": [
                    {
                        "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_4_front.jpg",
                        "position": 0
                    }
                ],
                "attributes": [
                    {
                        "id": 6,
                        "option": "black"
                    },
                    {
                        "name": "Size",
                        "option": "S"
                    }
                ]
            },
            {
                "regular_price": "19.99",
                "image": [
                    {
                        "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_3_front.jpg",
                        "position": 0
                    }
                ],
                "attributes": [
                    {
                        "id": 6,
                        "option": "green"
                    },
                    {
                        "name": "Size",
                        "option": "M"
                    }
                ]
            }
        ]}
        print(self.wcapi.post("products", data).json())

    # Read functions
    
    #Reads product list stored in WP site and populates local product info cache containers
    def populateProducts(self):
        self.set_allProductInfo(self.wcapi.get("products"))
        
        for pInfo in self.AllProductInfoList:
                self.ProductNameIdDict[pInfo.name] = pInfo.id
                
        return self.get_allProductInfo()
        
    def printAllProducts(self):
        print(self.wcapi.get("products").json())
        
    def getProductIdByName(self):
        pass
        
    # Update functions
    
    def updateProduct(self, productId, price, name, catId = "", category = "", catslug = ""):
        data = {
            "regular_price": price,
            "name" : name,
            "categories": [
                {
                  "id": catId,
                  "name": category,
                  "slug": catslug
                }]
        }
        print(self.wcapi.put(''.join(["products/", productId], data).json()))
    
    # Delete functions
    
    def deleteProduct(self, productId):
        return self.wcapi.delete(''.join(["products/" ,productId ,"?force=true"]).json())
        
    def deleteAllProducts(self):
        for product in self.getAllProducts():
            self.deleteProduct(product.id)
