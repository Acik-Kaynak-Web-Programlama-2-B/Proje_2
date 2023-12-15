from flask import Flask, render_template
import sqlite3


def take_data():
    connection_obj = sqlite3.connect('haberler.db')
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("SELECT * FROM Haberler_Tablosu")
    rows = cursor_obj.fetchall()
    connection_obj.close()  # Bağlantıyı kapatmayı unutmayın
    return rows

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("haber.html", data=take_data())


if __name__ == "__main__":
    app.run(debug=True)


