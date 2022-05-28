# Products Data - Scraping bestbuy
This script crawls though bestbuy and extracts the name , price, discount and link of each asus product

## tools used
- python programming
- playwright
- Beautiful soup

## project highlights
- import the necessary libraries
```python 
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
from openpyxl import Workbook
```

- The `download_html() ` takes a url as an urgument, navigates to the page, extracts the rendered html and sends it to the `parse_html()` function.
- The `parse_html()` scrapes the data and returns a link to the next page.
- The returned link by `parse_html()` is saved in a variable and used to access the next page for scraping.
```python
page.goto(next_page)
```
- The data is then saved in an excel file.
