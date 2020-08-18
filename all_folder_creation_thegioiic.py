import bs4
import pandas
import requests
from selenium import webdriver
import time
import os # write files
# from unidecode import unidecode
import math
import json
from unidecode import unidecode

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

# create product list main catgories
list_data = []
try:
  f = open('product.json', encoding="utf8")
  list_data = json.load(f)
  f.close()
except:
  print('product.json does not exist!')

# create main folders
if len(list_data) == 0:
  url = 'https://www.thegioiic.com/product' # input("Copy và dán link danh mục vào đây: ")
  # code = input("Nhập mã sản phẩm mới: ")
  soup = get_page_html(url)

  container = soup.find('div', class_='left-menu-new')
  items = container.findAll('a')

  urls = [item['href'] for item in items]
  category_names = [item.text.strip() for item in items]


  for i, name in enumerate(category_names):
    list_data.append({ 'number': i+1,
                      'name': name,
                      'foldername': unidecode(name).replace(' - ', ' ').replace(',', '').replace(' ', '_'),
                      'url': urls[i] })

  # print(code)
  print(list_data)

  # fo = open('product.py', 'w', encoding="utf-8") # create file
  # fo.write(f"list_data = {repr(list_data)}\n")
  if not os.path.exists('product.json'):
    with open('product.json', 'w', encoding='utf-8') as f:
      json.dump(list_data, f, ensure_ascii=False, indent=4)

  # create directories
  for list_item in list_data:
    if not os.path.exists(f"{list_item['number']}_{list_item['foldername']}"):
      os.mkdir(f"{list_item['number']}_{list_item['foldername']}")







##
## create child directories
##
code_index = 0
for list_item in list_data:
  child_list_data = []
  try:
    f = open(f"{list_item['number']}_{list_item['foldername']}/{list_item['foldername']}.json", encoding="utf8")
    child_list_data = json.load(f)
    f.close()
  except:
    print(f"{list_item['foldername']}.json does not exist!")

  if len(child_list_data) == 0:
    child_url = list_item['url']
    child_soup = get_page_html(child_url)

    child_container = child_soup.find('div', class_='left-menu-new')
    child_items = child_container.findAll('a')

    child_urls = [item['href'] for item in child_items]
    child_category_names = [item.text.strip() for item in child_items]
    
    for i, name in enumerate(child_category_names):
      child_list_data.append({
        'number': i+1,
        'name': name,
        'foldername': unidecode(name).replace(' - ', ' ').replace(',', '').replace(' ', '_'),
        'url': child_urls[i],
        'codeprefix': f"MUD{str(code_index).zfill(3)}A" })
      code_index += 1

    # print(code)
    print(child_list_data)

    # fo = open('product.py', 'w', encoding="utf-8") # create file
    # fo.write(f"list_data = {repr(list_data)}\n")
    if not os.path.exists(f"{list_item['number']}_{list_item['foldername']}/{list_item['foldername']}.json"):
      with open(f"{list_item['number']}_{list_item['foldername']}/{list_item['foldername']}.json", 'w', encoding='utf-8') as f:
        json.dump(child_list_data, f, ensure_ascii=False, indent=4)

    # create child directories
    for child_list_item in child_list_data:
      if not os.path.exists(f"{list_item['number']}_{list_item['foldername']}/{child_list_item['number']}_{child_list_item['foldername']}"):
        os.mkdir(f"{list_item['number']}_{list_item['foldername']}/{child_list_item['number']}_{child_list_item['foldername']}")


##
## create sub child directories's data files
##
for list_item in list_data:
  print(f"Entering {list_item['foldername']} folder...")

  child_list_data = []
  try:
    f = open(f"{list_item['number']}_{list_item['foldername']}/{list_item['foldername']}.json", encoding="utf8")
    child_list_data = json.load(f)
    f.close()
  except:
    print(f"{list_item['foldername']}.json does not exist!")
  
  for child_list_item in child_list_data:
    print(f"Entering {child_list_item['foldername']} folder...")
    print('')

    sub_child_list_data = []
    try:
      f = open(f"{list_item['number']}_{list_item['foldername']}/{child_list_item['number']}_{child_list_item['foldername']}/{child_list_item['foldername']}.json", encoding="utf8")
      sub_child_list_data = json.load(f)
      f.close()
    except:
      print(f"{child_list_item['foldername']}.json does not exist!")
  
    if len(sub_child_list_data) == 0:
      try:
        sub_child_url = child_list_item['url']
        sub_child_soup = get_page_html(sub_child_url)

        sub_child_container = sub_child_soup.find('div', class_='left-menu-new')
        print(sub_child_container)
        sub_child_items = sub_child_container.findAll('a')

        sub_child_urls = [item['href'] for item in sub_child_items]
        sub_child_category_names = [item.text.split(f" {item.text.split(' ')[-1]}")[0] for item in sub_child_items]
        numbers = [math.ceil(float(item.text.split(' ')[-1].replace('(', '').replace(')', '')) / 40) for item in sub_child_items]

        for i, name in enumerate(sub_child_category_names):
          sub_child_list_data.append({
            'name': name,
            'filename': child_list_item['foldername'],
            'url': sub_child_urls[i],
            'codeprefix': child_list_item['codeprefix'],
            'page': numbers[i] })
        
        print(sub_child_list_data)
        
        for sub_child_list_item in sub_child_list_data:
          if not os.path.exists(f"{list_item['number']}_{list_item['foldername']}/{child_list_item['number']}_{child_list_item['foldername']}/{child_list_item['foldername']}.json"):
            with open(f"{list_item['number']}_{list_item['foldername']}/{child_list_item['number']}_{child_list_item['foldername']}/{child_list_item['foldername']}.json", 'w', encoding='utf-8') as f:
              json.dump(sub_child_list_data, f, ensure_ascii=False, indent=4)
      except:
        print('Danh mục does not exist!')
