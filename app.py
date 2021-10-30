from flask import Flask, render_template, redirect, request
import sys
sys.path.insert(0, "backend/")
from db import db
app = Flask(__name__, template_folder='website')

@app.route('/')
@app.route('/index.html', methods = ['POST', 'GET'])
def index():
    if (request.method == 'GET'):
        if request.args.get('msg') == "error":
            return render_template("index.html", error_msg="Wrong username or password")
    return render_template("index.html")

@app.route('/CreateAccount.html')
def newAcc():
    return render_template("CreateAccount.html")

@app.route('/home.html', methods = ['POST', 'GET'])
def home():
    sql = db()
    if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        valid = sql.validate(username, password)
        sql.close()
        if valid == True:
            return render_template('home.html')
    
    return redirect('/index.html?msg=error')

if __name__ == "__main__":
    app.run(debug=True)