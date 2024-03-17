import pandas as pd
import sqlite3
import requests 
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attr = ['Name', 'MC_USD_Billion']
table = 'Largest_banks'
csv_path = 'Largest_Bank.csv'
xlsx_path = 'largest_Bank.xlsx'
conn = sqlite3.connect('database.db')

def extract(url, table_attr):
    response = requests.get(url)
    df = pd.DataFrame(columns = table_attr)
    data = BeautifulSoup(response.content, 'html.parser')
    tables = data.find_all('tbody')
    rows = tables[1].find_all('tr')
    data_list = []
    for row in rows:
        col = row.find_all('td')
        if len(col) >= 3:  # Kiểm tra xem có đủ cột không
            data_dict = {
                'Name': col[1].text.strip(),  # Trích xuất tên từ cột thứ hai
                'MC_USD_Billion': col[2].text.strip()
            }
            df1 = pd.DataFrame(data_dict, index = [0])
            df = pd.concat([df1, df], ignore_index = True)
    return df

df = extract(url, table_attr)
df.to_excel("Largest_Bank.xlsx")
    