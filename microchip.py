import bs4
import pandas
import requests

def get_page_content(url):
   page = requests.get(url,headers={"Accept-Language":"en-US"})
   return bs4.BeautifulSoup(page.text,"html.parser")

def get_page_details(paths):
  details = []
  for path in paths:
    url = "https://www.thegioiic.com" + path # các bạn thay link của trang mình cần lấy dữ liệu tại đây
    details.append(url)
  return details

names = []
desc_smalls = []
new_prices = []
amounts = []
paths = []

for page in range(1,10):
  url = "https://www.thegioiic.com/product/microchip?page=%d" % page # các bạn thay link của trang mình cần lấy dữ liệu tại đây
  soup = get_page_content(url)

  container = soup.find('div', {"id": "order_product"})
  products = container.findAll('p', class_='name-a')
  descriptions = container.findAll('div', class_='desc_small')
  price_tags = container.findAll('p', class_='price')
  prices = [int(price.text.strip().split(' ')[0].replace(',', '')) for price in price_tags]
  amount_tags = container.findAll('div', class_='contact-to-order-ab')

  

  names += [product.find('a').text for product in products]
  desc_smalls += [description.text.strip() for description in descriptions]
  new_prices += [int(round((price + price * 15 / 100)/500.0) * 500.0) for price in prices]
  amounts += [ 0 if len(amount.text.split(' ')) < 3 else int(amount.text.split(' ')[4]) for amount in amount_tags]

  paths += [product.find('a')['href'] for product in products]


df1 = pandas.DataFrame({'Danh mục':['Microchip' for name in names],
                        'Mã SP':['MUDA' + str(index).zfill(6) for index, name in enumerate(names)],
                        'Tên':names,
                        'Mô tả':desc_smalls,
                        'Giá bán':new_prices,
                        'Số lượng tồn':amounts,
                        'Link':get_page_details(paths)})

print(df1)

df1.to_excel('Microchip.xlsx')
