# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 13:45:08 2023

@author: C-117
"""

import sqlite3
from bs4 import BeautifulSoup
import requests

# Connect to SQLite database (it will be created if not exists)
conn = sqlite3.connect('haber.db')
cursor = conn.cursor()

# Create a table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS haberler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        baslik TEXT
    )
''')
conn.commit()

adres = "https://www.cnnturk.com/dunya-haberleri/"
sayfa = requests.get(adres)
icerik = BeautifulSoup(sayfa.text, "html.parser")
gerekli_kisim = icerik.find_all("div", {"class": "row slide-md-down"})

for item in gerekli_kisim:
    h3_element = item.find("figcaption", {"class": "card-caption"})
    if h3_element:
        haber_basligi = h3_element.text.strip()

        # Insert the data into the database
        cursor.execute('INSERT INTO haberler (baslik) VALUES (?)', (haber_basligi,))
        conn.commit()

        # Print the inserted data (optional)
        print(f"Inserted into database: {haber_basligi}")

# Close the database connection
conn.close()
