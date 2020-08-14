import bs4
import pandas
import requests

def get_page_content(url):
   page = requests.get(url,headers={"Accept-Language":"en-US"})
   return bs4.BeautifulSoup(page.text,"html.parser")

def get_page_details(paths):
  details = []
  for path in paths:
    url = "https://www.thegioiic.com" + path
    details.append(url)
  return details

names = []
desc_smalls = []
new_prices = []
amounts = []
paths = []
categories = []

array_data = [
	{ 'name': 'Microchip', 'url': 'https://www.thegioiic.com/product/microchip', 'page': 9,  },
	{ 'name': 'STMicroelectronics', 'url': 'https://www.thegioiic.com/product/stmicroelectronics-8c8b41d4-48b3-4510-87ea-74242d15c9b3', 'page': 3 },
	{ 'name': 'NXP', 'url': 'https://www.thegioiic.com/product/nxp-6e20e7a2-acb4-49ae-b9a4-c0ec119d5bd9', 'page': 1 },
	{ 'name': 'Nuvoton', 'url': 'https://www.thegioiic.com/product/nuvoton', 'page': 1 },
	{ 'name': 'Samsung', 'url': 'https://www.thegioiic.com/product/samsung', 'page': 1 },
	{ 'name': 'ICDREC', 'url': 'https://www.thegioiic.com/product/icdrec', 'page': 1 },
	{ 'name': 'Texas Instruments', 'url': 'https://www.thegioiic.com/product/texas-instruments-e4a66aff-1c5b-402b-8400-ca524144eba6', 'page': 1 },
	{ 'name': 'Intel', 'url': 'https://www.thegioiic.com/product/intel-1afb3aff-d03d-46ee-b24a-80e65807be5c', 'page': 1 },
	{ 'name': 'WIZnet', 'url': 'https://www.thegioiic.com/product/wiznet', 'page': 1 },
]

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
print(f"paths length = {len(get_page_details(paths))}")


df1 = pandas.DataFrame({'Danh mục':categories,
                        'Mã SP':['MUDA' + str(index).zfill(6) for index, name in enumerate(names)],
                        'Tên':names,
                        'Mô tả':desc_smalls,
                        'Giá bán':new_prices,
                        'Số lượng tồn':amounts,
                        'Link':get_page_details(paths)})

print(df1)

df1.to_excel('Microchip.xlsx')
