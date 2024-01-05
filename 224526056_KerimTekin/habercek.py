import sqlite3 
from bs4 import BeautifulSoup as bs
import requests

baglan = sqlite3.connect("tekonolojihaber.db")
cursor = baglan.cursor()

cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='haberler' ''')
if cursor.fetchone()[0] == 0:
    cursor.execute("""CREATE TABLE haberler(
        PkID INTEGER NOT NULL UNIQUE,
        Tarih TEXT NOT NULL,
        Baslik TEXT NOT NULL,
        Icerik TEXT NOT NULL,
        Link TEXT NOT NULL,
        PRIMARY KEY(PkID AUTOINCREMENT)
        )""")

haber = requests.get("https://www.klavyehaber.com/teknoloji/")
haber_veri = bs(haber.text,'html.parser')
haber_gerekli = haber_veri.findAll("div",{"class":"col-sm-6 col-xxl-4 post-col"})
link = []
baslik = []
icerik = []
saat = []


for i in haber_gerekli:
    teknoloji = i.find("div",{"class":"date"})
    teknoloji_gerekli = teknoloji.find("a")
    teknoloji_link = teknoloji_gerekli["href"]
    teknoloji_baslik = teknoloji_gerekli["title"]
    teknoloji_saat = teknoloji_gerekli.text
    link.append(teknoloji_link)
    baslik.append(teknoloji_baslik)
    saat.append(teknoloji_saat)
    x = requests.get(teknoloji_gerekli["href"])
    y = bs(x.text,'html.parser')
    if y.find("div",{"class":"entry-content"}):
        teknoloji_icerik = y.find("div",{"class":"entry-content"}).text
        icerik.append(teknoloji_icerik)
        
                     
for tarih, baslik, icerik, link in zip(saat, baslik, icerik, link):
    try:
        cursor.execute("SELECT * FROM haberler WHERE Tarih=? AND Baslik=? AND Icerik=? AND Link=?",
                       (tarih, baslik, icerik, link))
        varolan_kayit = cursor.fetchone()

        if varolan_kayit is None:
            cursor.execute("INSERT INTO haberler(Tarih, Baslik, Icerik, Link) VALUES (?, ?, ?, ?)",
                           (tarih, baslik, icerik, link))
    except Exception as e:
        print(f"Hata oluştu: {e}")

baglan.commit()
baglan.close()
    
    