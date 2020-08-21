import xlrd 
import json
from glob import glob

import os # write files

# get all main categories
list_data = []
try:
  file_name = glob("*.json")[0]
  f = open(file_name, encoding="utf8")
  list_data = json.load(f)
  f.close()
except:
  print(f"{file_name} does not exist!")

products_count = 0

# go inside every sub_child folder
##
## crawling every sub child category to get data product and images
##
for list_item in list_data:
  print(f"Entering {list_item['foldername']} folder...1")

  child_list_data = []
  try:
    f = open(f"{list_item['number']}_{list_item['foldername']}/{list_item['foldername']}.json", encoding="utf8")
    child_list_data = json.load(f)
    f.close()
  except:
    print(f"{list_item['foldername']}.json does not exist!")
  
  for child_list_item in child_list_data:
    print(f"Entering {child_list_item['foldername']} folder...2")

    # check if already have data excel and images
    check_excel_data = []
    file_name = ''
    try:
      file_name = glob(f"{list_item['number']}_{list_item['foldername']}/{child_list_item['number']}_{child_list_item['foldername']}/excels/*.json")[0]
      f = open(file_name, encoding="utf8")
      check_excel_data = json.load(f)
      f.close()
      print(f"{file_name} exists.")
    except:
      print(f"json data file does not exist!")
    
    # only crawl new data if does not have data
    print(f"Data exist length: {len(check_excel_data)}")
    print('')
    products_count += len(check_excel_data)

print(f"Total products = {products_count}")
exit()
