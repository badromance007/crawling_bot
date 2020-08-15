import bs4
import pandas
import requests
from selenium import webdriver
import time
# from unidecode import unidecode
from ic_programming import *

def get_page_content(url):
  page = requests.get(url,headers={"Accept-Language":"en-US"})
  return bs4.BeautifulSoup(page.text,"html.parser")

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

def get_page_details(paths):
  image_urls = []
  details = []
  for index, path in enumerate(paths):
    url = "https://www.thegioiic.com" + path

    # get detail
    soup = get_page_html(url)
    
    image_url = soup.find('div', class_='small-container').find('img')['src']

    detail = soup.find('div', class_='view_tab_product')

    print(f"{index}.Crawling -> {url}")
    print(f"{index}.{image_url}")

    # details.append(url)
    image_urls.append(image_url)
    details.append(detail)
  return [image_urls, details]

names = []
desc_smalls = []
new_prices = []
amounts = []
paths = []
categories = []
image_urls = []

array_data = list_data

def collect_data(array_data):
  global names
  global desc_smalls
  global new_prices
  global amounts
  global paths
  global categories

  for item in array_data:
    temp = []
    for page in range(1,(item['page']+1)):
      url = f"{item['url']}?page={page}"
      soup = get_page_content(url)

      container = soup.find('div', {"id": "order_product"})
      products = container.findAll('p', class_='name-a')
      descriptions = container.findAll('div', class_='desc_small')
      price_tags = container.findAll('p', class_='price')
      prices = [int(price.text.strip().split(' ')[0].replace(',', '')) for price in price_tags]
      amount_tags = container.findAll('div', class_='contact-to-order-ab')
      image_containers = container.findAll('div', class_='item-product-category')

      

      names += [product.find('a').text for product in products]
      desc_smalls += [description.text.strip() for description in descriptions]
      new_prices += [int(round((price + price * 15 / 100)/500.0) * 500.0) for price in prices]
      amounts += [ 0 if len(amount.text.split(' ')) < 3 else int(amount.text.split(' ')[4]) for amount in amount_tags]

      paths += [product.find('a')['href'] for product in products]

      print(url)
      temp += [item['name'] for product in products]
    
    # update categories
    categories += temp
    temp = []
    

# call function
collect_data(array_data)

print(f"categories length = {len(categories)}")
print(f"names length = {len(names)}")
print(f"desc_smalls length = {len(desc_smalls)}")
print(f"new_prices length = {len(new_prices)}")
print(f"amounts length = {len(amounts)}")
print(f"image_urls length = {len(image_urls)}")
print(f"paths length = {len(paths)}")


page_detail = get_page_details(paths)
df1 = pandas.DataFrame({'Danh mục':categories,
                        'Mã SP':[code + str(index).zfill(6) for index, name in enumerate(names)],
                        'Tên':names,
                        'Mô tả':desc_smalls,
                        'Giá bán':new_prices,
                        'Số lượng tồn':amounts,
                        'Ảnh':page_detail[0],
                        'Nội dung':page_detail[1]})

print(df1)

# df1.to_excel(f"{unidecode(filename).replace(',', '').replace(' ', '_')}.xlsx")
df1.to_excel(f"{filename}.xlsx")

# first time = 13m30s
# second time = 4m (+70% speed)
