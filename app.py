from flask import Flask, render_template, url_for, request, flash, current_app
import json, pymysql, os
from flaskext.mysql import MySQL

app = Flask(__name__)

app.secret_key = 'secret'
app.config['MYSQL_DATABASE_HOST'] = 'sql11.freemysqlhosting.net'
app.config['MYSQL_DATABASE_DB'] = 'sql11656172'
app.config['MYSQL_DATABASE_USER'] = 'sql11656172'
app.config['MYSQL_DATABASE_PASSWORD'] = 'tsG8aCb44p'

mysql = MySQL(app, cursorclass = pymysql.cursors.DictCursor)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_response = ''
    user_input = ''
    if request.method == 'POST':
        user_input = request.form['word']
        if user_input == '':
            flash('Please input a word!', 'flash-error')
        else:
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
    else:
        pass
        
    return render_template("Index.html", user_response = user_response, user_input = user_input)

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
    if word == '' or meaning == '':
        flash('Please fill out all fields!', 'flash-error')
    else:
        conn = mysql.get_db()
        cursor = conn.cursor()
        cursor.execute('insert into word(word, meaning) values(%s, %s)', (word, meaning))
        conn.commit()
        cursor.close()
        flash('Word succesfully added!', 'flash-success')

    return json.dumps('success')

@app.route('/add_logo', methods=['POST'])
def add_logo():
    image = request.files['file']

    if image:
        filepath = os.path.join( current_app.root_path, 'static/images/logo.png')
        image.save(filepath)
        flash('Success!', 'flash-success')
    else:
        flash('Error!', 'flash-error')

    return 'success'

@app.route('/word/<id>/delete', methods=['POST'])
def delete_word(id):
    word_id = id
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute('delete from word where id=%s', (word_id))
    conn.commit()
    cursor.close()
    flash('Word succesffuly deleted!', 'flash-success')

    return 'success'

@app.route('/word/<id>/edit', methods=['POST'])
def edit_word(id):
    word_id = id
    req = request.get_json()
    word = req['word']
    meaning = req['meaning']
    if word == '' or meaning == '':
        flash('Please fill out all fields!', 'flash-error')
    else:
        conn = mysql.get_db()
        cursor = conn.cursor()
        cursor.execute('update word set word=%s, meaning=%s where id=%s', (word, meaning, word_id))
        conn.commit()
        cursor.close()
        flash('Word succesffuly updated!', 'flash-success')

    return json.dumps('success')

if __name__ == "__main__":
    app.run(debug=True)