from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_input = ''
    if request.method == 'POST':
        user_input = request.form['word']
    return render_template("index.html", user_input = user_input)

@app.route('/dashboard')
def dashboard():
    return render_template("Dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)