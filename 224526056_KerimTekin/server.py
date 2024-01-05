from flask import * 
import sqlite3

def habercek():
    baglan = sqlite3.connect('tekonolojihaber.db')
    cursor = baglan.cursor()
    
    cekme = "SELECT * FROM haberler"
    cursor.execute(cekme)
    veriler = cursor.fetchall()
    baglan.close()
    return veriler

app = Flask(__name__)
@app.route("/")
def anasayfa():
    return render_template("haberler.html",veri = habercek())

if __name__ == '__main__':
    app.run(debug=True)


