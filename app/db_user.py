import sqlite3

DB_FILE="user.db"

db = sqlite3.connect(DB_FILE,check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

# db.execute("DROP TABLE if exists usernames")
# db.execute("DROP TABLE if exists blog")
c.execute("CREATE TABLE IF NOT EXISTS usernames(user TEXT UNIQUE, pass TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS blog(user TEXT, title TEXT, content TEXT, date_added INTEGER, data_mod INTEGER,view_count INTEGER, time INTEGER, id INTEGER PRIMARY KEY AUTOINCREMENT, slug TEXT UNIQUE)")

#check if username in table: (helper function)
def in_table(username):
    user_list = list(c.execute("SELECT user FROM usernames").fetchall())
    print(user_list)
    for i in user_list:
        for j in i:
            if username == j:
                return True
    return False

#adds new username and password to table if not exist
def add_to_db(username,password):
    if (username == "") or (password == ""):
        return False
    if in_table(username): 
        return False
    else:
        c.execute("INSERT INTO usernames VALUES(?,?)",(username,password))
        # c.execute(f'INSERT INTO usernames VALUES("{username}","{password}")')
    db.commit() 
    return True

#gets password of username: (helper function)
def get_pass(username):
    if in_table(username):
        user_list = list(c.execute("SELECT * FROM usernames").fetchall())
        for i in user_list:
            if i[0] == username:
                return i[1]
    return False

def make_slug(title):
    return title.lower().replace(" ","-")

#check if password is correct
def correct_pass(username,password):
    return get_pass(username) == password

#get all usernames
def get_users():
    return c.execute("SELECT * FROM usernames").fetchall()


#add post to blog 
def add_post(username,title,content,date_added,data_mod,view,time):
    # don't use f strings to insert variables into SQL queries 
    c.execute("INSERT INTO blog VALUES(?,?,?,?,?,?,?,NULL,?)",(username,title,content,date_added,data_mod,view,time,make_slug(title)))
    db.commit() 

#gets all posts from blog
def get_posts():
    # sorted by latest to oldest
    return c.execute("SELECT * FROM blog ORDER BY time DESC").fetchall()

#get all posts from user
def get_user_posts(name):
    # sorted by latest to oldest
    return c.execute("SELECT * FROM blog WHERE user=? ORDER BY time DESC",(name,)).fetchall()

#allow post author to edit post
def edit_post(username,title,content,date_added,data_mod,time):
    if in_table(username):
        c.execute("UPDATE blog SET title=?, content=?, date_added=?, data_mod=? WHERE time=?",(title,content,date_added,data_mod,time))
        db.commit() 
        return True
    return False

#search for posts by title or content
def search_posts(search):
    return c.execute("SELECT * FROM blog WHERE title=?",(search,)).fetchall()

#delete post
def delete_post(username,title):
    if in_table(username):
        c.execute('DELETE FROM blog WHERE title=?',(title,))
        db.commit() 
        return True
    return False

#get post author
def get_author(slug):
    return list(c.execute(f'SELECT user FROM blog WHERE slug="{slug}"').fetchall())[0][0]

#increment number of views (old)
def increment_views(slug):
    c.execute(f'UPDATE blog SET num_view=num_view+1 WHERE slug="{slug}"')
    db.commit()

# get one post by slug
def get_post(slug):
    return list(c.execute("SELECT * FROM blog WHERE slug=?",(slug,)).fetchall())[0]

def get_unix(slug):
    c.execute('SELECT time FROM blog WHERE slug=?',(slug,))

def get_date_added(slug):
    c.execute('SELECT date_added FROM blog WHERE slug=?',(slug,))

def get_title(slug):
    return list(c.execute("SELECT * FROM blog WHERE slug=?",(slug,)).fetchall())[0][1]


db.commit() #save changes

#db.close()  #close database
#command = ""          # test SQL stmt in sqlite3 shell, save as string
#c.execute(command)    # run SQL statement


# Tests
add_to_db("DWM", "ABC")
#add_post("DWM", "Test 1", "hello world", 11, 11, 0, 1123)
print(get_users())
print(c.execute('SELECT date_added FROM blog WHERE slug="{stuyvesant-test}"'))