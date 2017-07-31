from Controllers.ProductScraper import ProductScraper
from Controllers.WordPressController import WordPressController

def main():
    p = ProductScraper()
    p.runProc()
    
    w = WordPressController()
    #w.createSimpleProduct("Super Bud A", "2.99")
    w.printAllProducts()
    
if __name__ == "__main__":
    main()
