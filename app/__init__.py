# David Chen, William Guo, Marc Jiang
# Disturbed Window Monsters
# SoftDev
# Nov 03 2022


from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import request, Response, redirect, session, url_for  # facilitate form submission
from db_user import add_to_db, correct_pass, in_table, add_post, get_posts
import datetime, time

# the conventional way:
#from flask import Flask, render_template, request
#username = "DWM"
#password = "ABC"

app = Flask(__name__)  # create Flask object
app.secret_key = "m4Wa0SY66R34R2fbty7P5Nmxg8fLNOQ6"

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)  # displays app
    print("***DIAG: request obj ***")
    print(request)  # displays page request
    print("***DIAG: request.args ***")
    print(request.args)
    # print("***DIAG: request.args['username']  ***")
    # print(request.args['username'])
    print("***DIAG: request.headers ***")
    print(request.headers)

    if "username" in session:
        return render_template('index.html', success=True, data = get_posts())
    else:
        return render_template('index.html', success=False)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if "username" in session:
            return render_template('index.html', success=True)
        else:
            return render_template('login.html')
    elif request.method == "POST":
        print("\n\n\n")
        print("***DIAG: this Flask obj ***")
        print(app)
        print("***DIAG: request obj ***")
        print(request)
        print("***DIAG: request.args ***")
        print(request.form)  # displays entered info as dict
        print("***DIAG: request.args['username']  ***")
        print(request.form['username'])
        print("***DIAG: request.headers ***")

    username = request.form['username']
    password = request.form['password']
    if in_table(username):
        if correct_pass(username,password):
            session["username"] = request.form.get("username")
            return redirect("/")
        else:
            return render_template('index.html', success=False, message="Incorrect Password")
    else:
        return render_template('index.html', success=False, message="Username does not exist")

@app.route("/logout", methods=['POST'])
def logout():
    if request.method != "POST":
        return Response(status=405)
    print(request.form)  # displays entered info as dict
    if "username" in session:
        session.pop("username")
    return redirect("/")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    elif request.method == "POST":
        print("\n\n\n")
        print("***DIAG: this Flask obj ***")
        print(app)
        print("***DIAG: request obj ***")
        print(request)
        print("***DIAG: request.args ***")
        print(request.form)
        print("***DIAG: request.args['username']  ***")
        print(request.form['username'])
        print("***DIAG: request.headers ***")
        # use helper functions from db_user.py to add user to database
        if add_to_db(request.form['username'], request.form['password']):
            return render_template('index.html', success=True, message="Successful")
        else:
            return render_template('index.html', success=False, message="Username already exists")
    else:
        return Response(status=405)

@app.route("/blog", methods=['GET', 'POST'])
def disp_blogpage():
    if request.method == "GET":
        return render_template('blog.html')
    elif request.method == "POST":
        print("\n\n\n")
        print("***DIAG: this Flask obj ***")
        print(app)
        print("***DIAG: request obj ***")
        print(request)
        print("***DIAG: request.args ***")
        print(request.form)
        print("***DIAG: request.args['username']  ***")
        print(request.form['username'])
        print("***DIAG: request.headers ***")
        # use helper functions from db_user.py to add new blog post to database

        #BIG_NOTE: FIX THIS ISSUE OF 'TypeError: add_post() takes 7 positional arguments but 9 were given'



        #if add_post(request.form['username'], request.form['title'],request.form['context'],request.form['date'],request.form['date'],0,datetime.datetime.now()):
        #    return render_template('index.html', success=True)
        #else:
        return render_template('index.html',success=True)
    else:
        return Response(status=405)



if __name__ == "__main__":  # false if this file imported as module
    # enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
