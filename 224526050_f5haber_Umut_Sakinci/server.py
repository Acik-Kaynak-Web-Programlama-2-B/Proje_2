from flask import*
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('haberler.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)


@app.route('/')
def index():
    conn = get_db_connection()
    haberler = conn.execute('SELECT * FROM haberler').fetchall()
    conn.close()
    return render_template('index.html',haberler=haberler)


if __name__ == '__main__':
    app.debug = True
    app.run(host="localhost", port=5000)