from flask import Flask, render_template, url_for, request
import datetime, json
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'dictionary'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'

mysql = MySQL(app, cursorclass = pymysql.cursors.DictCursor)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_response = ''
    user_input = ''
    if request.method == 'POST':
        user_input = request.form['word']
        conn = mysql.get_db()
        cursor = conn.cursor()
        cursor.execute('select meaning from dictionary.word where word=%s', (user_input))
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        if (len(result) > 0):
            user_response = result[0]['meaning']
        else:
            user_response = 'This word does not exist in this dictionary, try another word'
        
    return render_template("index.html", user_response = user_response, user_input = user_input)

@app.route('/dashboard')
def dashboard():
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute('select * from dictionary.word')
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template("Dashboard.html", entries = result)

@app.route('/word', methods=['POST'])
def add_word():
    req = request.get_json()
    word = req['word']
    meaning = req['meaning']
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute('insert into word(word, meaning) values(%s, %s)', (word, meaning))
    conn.commit()
    cursor.close()

    return json.dumps('success')

@app.route('/word/<id>/delete', methods=['POST'])
def delete_word(id):
    word_id = id
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute('delete from word where id=%s', (word_id))
    conn.commit()
    cursor.close()

    return json.dumps('success')

if __name__ == "__main__":
    app.run(debug=True)