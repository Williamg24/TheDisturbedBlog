# David Chen, William Guo, Marc Jiang
# Disturbed Window Monsters
# SoftDev
# Nov 03 2022


from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import request, Response, redirect, session, url_for  # facilitate form submission
from db_user import add_to_db, correct_pass, in_table, add_post, get_posts,get_post,get_user_posts
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
    print(get_posts())
    if "username" in session:
        return render_template('index.html', success=True, blogs = get_user_posts(session.get('username')))
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
        return render_template('blog.html', username = session.get('username'))
    elif request.method == "POST":
        print("\n\n\n")
        print("***DIAG: this Flask obj ***")
        print(app)
        print("***DIAG: request obj ***")
        print(request)
        print("***DIAG: request.args ***")
        print(request.form)
        print("***DIAG: request.args['username']  ***")
        #print(request.form['username'])
        print("***DIAG: request.headers ***")
        # use helper functions from db_user.py to add new blog post to database
        if add_post(session.get("username"),request.form['title'],request.form['content'],datetime.datetime.now(),datetime.datetime.now(),0,datetime.datetime.now()):
            return render_template('index.html', success=False, message="Failed")
        else:
            return redirect('/')
    else:
        return Response(status=405)

@app.route("/view", methods=['GET', 'POST'])
def view():
    if request.method == "GET":
        return render_template('view.html', blogs = get_posts())
    elif request.method == "POST":
        print("\n\n\n")
        print("***DIAG: this Flask obj ***")
        print(app)
        print("***DIAG: request obj ***")
        print(request)
        print("***DIAG: request.args ***")
        print(request.form)
        print("***DIAG: request.args['username']  ***")
        #print(request.form['username'])
        print("***DIAG: request.headers ***")
        # use helper functions from db_user.py to add new blog post to database
    else:
        return Response(status=405)

#dynamic routing for blog posts (blog/<slug>)
@app.route("/blog/<slug>", methods=['GET', 'POST'])
def disp_blogpost(slug):
    if request.method == "GET":
        return render_template('blogpost.html', username = session.get('username'), slug = slug, blog = get_post(slug))
    else:
        return Response(status=405)

@app.route("/help", methods=['GET', 'POST'])
def help():
    return render_template('help.html')

@app.route("/back", methods=['GET', 'POST'])
def back():
    return redirect('/')

@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == "GET":
        return render_template('edit.html', blogs = get_user_posts(session.get('username')))
    elif request.method == "POST":
        print("\n\n\n")
        print("***DIAG: this Flask obj ***")
        print(app)
        print("***DIAG: request obj ***")
        print(request)
        print("***DIAG: request.args ***")
        print(request.form)
        print("***DIAG: request.args['username']  ***")
        #print(request.form['username'])
        print("***DIAG: request.headers ***")
        # use helper functions from db_user.py to add new blog post to database
    else:
        return Response(status=405)

if __name__ == "__main__":  # false if this file imported as module
    # enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
