from bs4 import BeautifulSoup
import requests
import sqlite3

url = "https://www.f5haber.com/"
request = requests.get(url)

soup = BeautifulSoup(request.content, 'html.parser')




haberler = soup.find("div", {"class":"infinity-item"}).findAll("div",{"class":"post post-list"})
links= [haber.find("a")["href"] for haber in haberler]
titles= [haber.find("a")["title"] for haber in haberler]
summaries = [haber.find("span", {"class": "summary"}).get_text() for haber in haberler]
dates = [haber.find("time").get_text() for haber in haberler]

conn = sqlite3.connect('haberler.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS haberler
                      (PkID INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT ,
                       link TEXT ,
                       summary TEXT, 
                       date TEXT )''')
for link, title,summary,date in zip(links, titles,summaries,dates):
    cursor.execute("INSERT INTO haberler (title, link, summary, date) VALUES (?, ?, ?, ?)", (title, link,summary, date))

conn.commit()

conn.close()

