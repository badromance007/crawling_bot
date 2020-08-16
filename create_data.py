import bs4
import pandas
import requests
from selenium import webdriver
import time
import os # write files
# from unidecode import unidecode
import math

def get_page_html(url):
  options = webdriver.ChromeOptions()
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--incognito')
  options.add_argument('--headless')
  options.add_argument('--no-sandbox') # Bypass OS security model
  driver = webdriver.Chrome("chromedriver.exe", options=options)
  
  driver.get(url)
  time.sleep(1)
  page = driver.page_source
  # driver.quit()
  
  return bs4.BeautifulSoup(page,"lxml")

url = input("Copy và dán link danh mục vào đây: ")
code = input("Nhập mã sản phẩm mới: ")
soup = get_page_html(url)

container = soup.find('div', class_='left-menu-new')
items = container.findAll('a')

title = soup.find('h1', {"class": "h1-title"}).text
urls = [item['href'] for item in items]
category_names = [item.text.split(f" {item.text.split(' ')[-1]}")[0] for item in items]
numbers = [math.ceil(float(item.text.split(' ')[-1].replace('(', '').replace(')', '')) / 40) for item in items]

list_data = []
for i, name in enumerate(category_names):
  list_data.append({ 'name': name, 'url': urls[i], 'page': numbers[i]})

print(title)
print(code)
print(list_data)

fo = open('data/data.py', 'w', encoding="utf-8") # create file
fo.write(f"list_data = {repr(list_data)}\n" + f"code = {repr(code)}\n" + f"filename = {repr(title)}\n")
