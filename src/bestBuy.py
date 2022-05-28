from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
from openpyxl import Workbook

wb =Workbook()
ws = wb.active
ws.append(['NAME','PRICE','DISCOUNT','LINK'])

URL = 'https://www.bestbuy.com/'

def download_html(url):

    playwright = sync_playwright().start()
    browser = playwright.firefox.launch(headless=False,slow_mo=50)
    page = browser.new_page()

    page.goto("https://www.bestbuy.com/")
    #choose a country
    page.locator("text=Hello! Choose a country. Canada United States Mexico Shopping in the U.S.? Inter >> img[alt=\"United States\"]").click()
    #search for asus products
    page.locator("[placeholder=\"Search Best Buy\"]").click()
    page.locator("[placeholder=\"Search Best Buy\"]").fill("asus")
    page.locator("[placeholder=\"Search Best Buy\"]").press("Enter")

    time.sleep(3)
    #########################################
    #############   PAGINATION  #############
    #########################################
    #pass the html into the parser and expect a url to the next page
    page.wait_for_selector('div.component-sku-list')
    
    html = page.inner_html('div.component-sku-list')

    #print(html)
    #python does not have a do while loop
    #so i implement one
    next_page = parse_html(html)#returns a link to the next page
    while next_page:#while the return value is not none
        print('scraping next page...')
        page.goto(next_page)
        #extract the html and send it to parse_html
        page.wait_for_selector('div.component-sku-list')
        

        html = page.inner_html('div.component-sku-list')
        next_page = parse_html(html)
    browser.close()


def parse_html(html):
    
    soup= BeautifulSoup(html,'html.parser')
    tags = soup.find_all('li','embedded-sponsored-listing')+soup.find_all('li','sku-item')
    print(len(tags))
    for tag in tags:
        #start selecting the data we want
        if tag.name:

            name_tag = tag.find('h4','sku-title')
            name = name_tag.get_text() if name_tag else None

            price_tag = tag.find('div','priceView-hero-price')
            price = price_tag.span.get_text() if price_tag else None

            discount_tag  = tag.find('div','pricing-price__savings')
            discount = discount_tag.get_text().split('$')[-1] if discount_tag else 0
            
            link = 'https://www.bestbuy.com'+name_tag.a.get('href') if name_tag else None
            #save in an excel file
            if name and price and link:

                ws.append([name,price,'$'+str(discount),link])
                wb.save('AsusProducts.xlsx')
    next_page = soup.find('a',attrs={"class":"sku-list-page-next","aria-disabled":"false"})
    return 'https://www.bestbuy.com'+next_page.get('href') if next_page else None




def main(url):
    download_html(url)
    
if __name__=='__main__':
    main(URL)
