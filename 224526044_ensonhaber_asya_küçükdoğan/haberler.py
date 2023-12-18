import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

url = "https://www.ensonhaber.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


baglan = sqlite3.connect("haberler.db")
cursor = baglan.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS haberler (
                    PkID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Baslik TEXT NOT NULL,
                    Link TEXT NOT NULL,
                    Icerik TEXT NOT NULL,
                    Tarih TEXT NOT NULL,
                    Saat TEXT NOT NULL
                )""")


haber_bolumu = soup.find("section", class_="mb-30")
if haber_bolumu:

    haberler = haber_bolumu.find_all("div", class_="item")

    for haber in haberler:

        baslik = haber.find("span", class_="text").text.strip()
        link = "https://www.ensonhaber.com" + haber.find("a")["href"]


        haber_link = "https://www.ensonhaber.com" + haber.find("a")["href"]
        haber_response = requests.get(haber_link)
        haber_soup = BeautifulSoup(haber_response.text, 'html.parser')


        tarih_saat_etiketi = haber_soup.find("div", class_="article-date").find("time")
        if tarih_saat_etiketi:
            tarih_saat = tarih_saat_etiketi.get("datetime")
            tarih_obj = datetime.strptime(tarih_saat, "%Y-%m-%dT%H:%M:%S%z")
            tarih = tarih_obj.strftime("%d.%m.%Y")
            saat = tarih_obj.strftime("%H:%M")


            haber_icerik = haber_soup.find("div", class_="article-body")
            if haber_icerik:
                icerik = haber_icerik.text.strip()
            else:
                icerik = "İçerik bulunamadı."

            cursor.execute("INSERT INTO haberler(Baslik, Link, Icerik, Tarih, Saat) VALUES (?, ?, ?, ?, ?)",
                           (baslik, link, icerik, tarih, saat))

            print(f"Haber ekleniyor: {baslik}")


baglan.commit()
baglan.close()
