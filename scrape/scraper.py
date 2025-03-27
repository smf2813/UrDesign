from playwright.sync_api import sync_playwright, Playwright
from rich import print 

def run(playwright: Playwright):
    start_url='https://www.rcity.co.il/en/product-category/%d7%9e%d7%99%d7%98%d7%95%d7%aa/'
    chrome = playwright.chromium
    browser = chrome.launch(headless=False)
    page = browser.new_page()
    page.goto(start_url)

with sync_playwright() as p:
    run(p)