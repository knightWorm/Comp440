from flask import Flask, render_template, redirect, request, session
import sys, json
sys.path.insert(0, "backend/")
from db import db
config = json.load(open('backend/private.json'))
app = Flask(__name__, template_folder='website')
app.config["SECRET_KEY"] = config['password']
sql = db()
sql.reset()
sql.close()

@app.route('/')
@app.route('/index.html', methods = ['POST', 'GET'])
def index():
    if (request.method == 'GET'):
        if request.args.get('msg') == "error":
            return render_template('/index.html', error_msg="Wrong username or password")
    return render_template('/index.html')

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

    return render_template('CreateAccount.html')

@app.route('/blog.html', methods=['POST','GET'])
def blog():
    # Signing in/out
    username = request.form.get('username')
    password = request.form.get('password')
    signout = request.form.get('sign_out')

    # Creating a new blog
    blog = request.form.get('create_blog')
    subject = request.form.get('subject')
    description = request.form.get('blog')
    tags = request.form.get('tag')

    # Selecting blog
    select = request.args.get('searchblogs')

    sql = db()
    # If user is signed in
    if 'username' in session and username == None and password == None:
        if (request.method == 'POST'):
            # Create a blog
            if blog == 'true':
                sql.create_blog(subject, description, tags, session['username'])
                sql.close()
            # Signout
            elif signout == 'true':
                session.pop('username', None)
                return redirect('/')
        elif (request.method == 'GET'):
            if select:
                return render_template('blog.html', options=sql.get_options(), blog=sql.get_blog(select))
        return render_template('blog.html', options=sql.get_options())

    # If user is not signed in
    elif (request.method == 'POST'):
        valid = sql.validate(username, password)
        sql.close()
        if valid == True:
            session['username'] = username
            return render_template('blog.html')
        else: 
            return redirect('/index.html?msg=error')
    return redirect('/')
    
@app.route('/home.html', methods = ['POST', 'GET'])
def home():
    username = request.form.get('username')
    password = request.form.get('password')
    reset = request.form.get('reset_DB')
    signout = request.form.get('sign_out')
    if 'username' in session and username == None and password == None:
        if (request.method == 'POST'):
            if reset == 'true':
                sql = db()
                sql.reset()
                sql.close()
                return render_template('home.html')
            elif signout == 'true':
                session.pop('username', None)
                return redirect('/index.html')
        else:
            return render_template('home.html')
        
    elif (request.method == 'POST'):
        sql = db()
        valid = sql.validate(username, password)
        sql.close()
        if valid == True:
            session['username'] = username
            return render_template('blog.html')
    
    return redirect('/index.html?msg=error')

@app.route('/backendOperations.html')
def tempPage():
    # if (request.method == 'GET'):
    #     return render_template('baclendOperations.html')
    
    return render_template('backendOperations.html')

if __name__ == "__main__":
    app.run(debug=True)