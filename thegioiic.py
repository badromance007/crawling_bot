import bs4
import pandas
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
# import time
import os # write files
from tqdm import tqdm # for images downloading progress bar
from unidecode import unidecode
from data.data import *

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
  # time.sleep(1)
  delay = 30 # seconds
  try:
    # WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.show-small-img')))
    small_images = driver.find_elements_by_css_selector(".show-small-img")
    for image in small_images:
      print(f"Before Waiting /images/loader.gif => {image.get_attribute('src')}")
      WebDriverWait(driver, delay).until(lambda x: '/images/loader.gif' not in image.get_attribute('src'))
      print(f"After Waiting /images/loader.gif => {image.get_attribute('src')}")
    print("Page is ready!")
  except TimeoutException:
    print("Loading took too much time!")
  page = driver.page_source
  # driver.quit()
  
  return bs4.BeautifulSoup(page,"lxml")

def download(image_url, pathname, name):
  # Downloads an image given an URL and puts it in the folder `images`
  # if images doesn't exist, make that images dir
  if not os.path.isdir(pathname):
    print('Create images folder!')  
    os.makedirs(pathname)
  response = requests.get(image_url, stream=True) # download response body
  file_size = int(response.headers.get("Content-Length", 0)) # get filesize
  filename = os.path.join(pathname, f"{name}.{image_url.split('.')[-1]}") # # get the file name
  # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
  progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
  with open(filename, "wb") as f:
      for data in progress:
          # write data read to the file
          f.write(data)
          # update the progress bar manually
          progress.update(len(data))

def get_page_details(paths, product_codes):
  image_amounts = []
  details = []
  for index, path in enumerate(paths):
    url = "https://www.thegioiic.com" + path

    # get detail
    soup = get_page_html(url)
    
    image_tags = soup.find('div', class_='small-container').findAll('img')
    image_urls = [image_tag['src'] for image_tag in image_tags]
    for i, image_url in enumerate(image_urls):
      if i == 0:
        download(image_url, 'images', product_codes[index]) # download first images
      else:
        download(image_url, 'images', f"{product_codes[index]}_{i}") # download remaining images

    detail = soup.find('div', class_='view_tab_product')

    print(f"{index}.Crawling -> {url}")
    for image_url in image_urls:
      print(f"{index}.{image_url}")

    # details.append(url)
    image_amounts.append(len(image_urls))
    details.append(detail)
  return [image_amounts, details]

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

product_codes = [code + str(index).zfill(6) for index, name in enumerate(names)]
page_detail = get_page_details(paths, product_codes)
df1 = pandas.DataFrame({'Danh mục cấp 1':['' for category in categories],
                        'Danh mục cấp 2':['' for category in categories],
                        'Danh mục cấp 3':categories,
                        'Mã SP':product_codes,
                        'Tên':names,
                        'Mô tả':desc_smalls,
                        'Giá bán':new_prices,
                        'Số lượng tồn':amounts,
                        'Số lượng ảnh':page_detail[0],
                        'Nội dung':page_detail[1]})

print(df1)

df1.to_excel(f"excels/{unidecode(filename).replace(',', '').replace(' ', '_')}.xlsx")
# df1.to_excel(f"excels/{filename}.xlsx")

# first time = 13m30s
# second time = 4m (+70% speed)
