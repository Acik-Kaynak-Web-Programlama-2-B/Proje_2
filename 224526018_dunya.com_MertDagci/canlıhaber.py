import requests
from bs4 import BeautifulSoup
import sqlite3


def scraping():
    news_list = []

    x = requests.get("https://www.dunya.com/gundem")
    soup = BeautifulSoup(x.text, "html.parser")

    news_elements = soup.find_all("span", {"class": "big"})
    desc_elements = soup.find_all("span", {"class": "desc"})
    time_elements = soup.find_all("time", {"class": "pubdate"})  
    link_elements = soup.find_all("a", {"href":""})
   

    for title, desc, time_element in zip(news_elements, desc_elements, time_elements):
        news_list.append({
        "title": title.text.strip(),
        "contents": desc.text.strip(),
        "publish_time": time_element["datetime"],
        "link": title.find('a')['href']  
    })


    return news_list

baglanti = sqlite3.connect('haberler.db')
cursor = baglanti.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Haberler_Tablosu (
    pkID INTEGER PRIMARY KEY AUTOINCREMENT,
    Baslik TEXT NOT NULL,
    Icerik TEXT NOT NULL,
    Yayin_Zamani TEXT,
    Link TEXT  
);""")


headlines = scraping()
for news in headlines:
    title = news["title"]
    contents = news["contents"]
    publish_time = news["publish_time"]
    link = news["link"]  # Eklenen link bilgisi
    cursor.execute("INSERT INTO Haberler_Tablosu (Baslik, Icerik, Yayin_Zamani, Link) VALUES (?, ?, ?, ?)",
                   (title, contents, publish_time, link))


baglanti.commit()
baglanti.close()


