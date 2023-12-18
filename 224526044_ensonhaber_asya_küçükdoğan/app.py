from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    baglan = sqlite3.connect("haberler.db")
    cursor = baglan.cursor()

    cursor.execute("SELECT Baslik, Link, Icerik, Tarih, Saat FROM haberler")
    haberler = cursor.fetchall()

    baglan.close()

    return render_template('index.html', haberler=haberler)

if __name__ == '__main__':
    app.run(debug=True)

