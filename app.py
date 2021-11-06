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

@app.route('/CreateAccount.html', methods = ['POST', 'GET'])
def newAcc():        
    if (request.method == 'POST'):
        sql = db()
        username = request.form.get('createUsername')
        password = request.form.get('createPassword')
        first = request.form.get('fname')
        last = request.form.get('lname')
        email = request.form.get('createEmail')

        duplicates = sql.get_duplicates(username, email)
        if duplicates == False:
            sql.create_account(username, password, first, last, email)
            sql.close()
            return redirect('/index.html')
        else:
            sql.close()
            return redirect('/CreateAccount.html?msg=dup')

    elif (request.method == 'GET'):
        if request.args.get('msg') == "dup":
            return render_template("CreateAccount.html", error_msg="Username or email is already in use")

    return render_template("CreateAccount.html")

@app.route('/home.html', methods = ['POST', 'GET'])
def home():
    if (request.method == 'POST'):
        sql = db()
        username = request.form.get('username')
        password = request.form.get('password')
        if username == None or password == None:
            sql.reset()
            sql.close()
            return render_template('home.html')
        else:
            valid = sql.validate(username, password)
            sql.close()
            if valid == True:
                return render_template('home.html')
    
    return redirect('/index.html?msg=error')

if __name__ == "__main__":
    app.run(debug=True)