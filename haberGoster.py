from flask import Flask, render_template
import sqlite3
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def take_data():
    connection_obj = sqlite3.connect('haberler.db')
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("SELECT * FROM Haberler_Tablosu")
    rows = cursor_obj.fetchall()
    connection_obj.close()  # Bağlantıyı kapatmayı unutmayın
    return rows

def scraping():
    news_list = []

    x = requests.get("https://www.dunya.com/gundem")
    soup = BeautifulSoup(x.text, "html.parser")

    news_elements = soup.find_all("span", class_=["big", "xbig"])
    # desc_elements = soup.find_all("span", {"class": "desc"})
   
    for title in zip(news_elements):
        desc = title[0].parent.find_all("span", {"class": "desc"})[0].text.strip()
        news_list.append({
        "title": title[0].text.strip(),
        "contents": desc,
        "publish_time": "",
        "link": title[0].parent.parent.get("href"),
    })
    
    for news in news_list:
        x = requests.get(news["link"])
        soup = BeautifulSoup(x.text, "html.parser")
        time_element = soup.find("time", {"class": "pubdate"})
        news["publish_time"] = time_element.text.strip()
    
    return news_list

def insert_data():
    baglanti = sqlite3.connect('haberler.db')
    cursor = baglanti.cursor()
    headlines = scraping()
    cursor.execute("DELETE FROM Haberler_Tablosu")
    baglanti.commit()
    
    for news in headlines:
        title = news["title"]
        contents = news["contents"]
        publish_time = news["publish_time"]
        link = news["link"]  # Eklenen link bilgisi
        cursor.execute("INSERT INTO Haberler_Tablosu (Baslik, Icerik, Yayin_Zamani, Link) VALUES (?, ?, ?, ?)",
                (title, contents, publish_time, link))


    baglanti.commit()
    baglanti.close()

    return

@app.route('/')
def index():
    insert_data()
    return render_template("haber.html", data=take_data())


if __name__ == "__main__":
    app.run(debug=True, use_debugger=True, use_reloader=False)


