import sqlite3

DB_FILE="user.db"

db = sqlite3.connect(DB_FILE,check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

db.execute("DROP TABLE if exists usernames")
db.execute("DROP TABLE if exists blog")
c.execute("CREATE TABLE usernames(user TEXT UNIQUE, pass TEXT)")
c.execute("CREATE TABLE blog(user TEXT, title TEXT, content TEXT, date_added INTEGER, data_mod INTEGER, num_view INTEGER, time INTEGER, id INTEGER PRIMARY KEY AUTOINCREMENT, slug TEXT UNIQUE)")

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
        c.execute(f'INSERT INTO usernames VALUES("{username}","{password}")')
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

#check if password is correct
def correct_pass(username,password):
    return get_pass(username) == password

#get all usernames
def get_users():
    return c.execute("SELECT * FROM usernames").fetchall()


#add post to blog 
def add_post(username,title,content,date_added,data_mod,num_view,time):
    c.execute(f'INSERT INTO blog VALUES("{username}","{title}","{content}","{date_added}","{data_mod}","{num_view}","{time}")')
    db.commit() 

#gets all posts from blog
def get_posts():
    # sorted by latest to oldest
    return list(c.execute("SELECT * FROM blog ORDER BY time DESC").fetchall())

#allow post author to edit post
def edit_post(username,title,content,date_added,data_mod,num_view,time):
    if in_table(username):
        c.execute(f'UPDATE blog SET title="{title}", content="{content}", date_added="{date_added}", data_mod="{data_mod}", num_view="{num_view}" WHERE time="{time}"')
        db.commit() 
        return True
    return False

#search for posts by title or content
def search_posts(search):
    return list(c.execute(f'SELECT * FROM blog WHERE title LIKE "%{search}%" OR content LIKE "%{search}%"').fetchall())

#delete post
def delete_post(username,time):
    if in_table(username):
        c.execute(f'DELETE FROM blog WHERE time="{time}"')
        db.commit() 
        return True
    return False

#get post author
def get_author(slug):
    return list(c.execute(f'SELECT user FROM blog WHERE slug="{slug}"').fetchall())[0][0]

#increment number of views
def increment_views(slug):
    c.execute(f'UPDATE blog SET num_view=num_view+1 WHERE slug="{slug}"')
    db.commit()

db.commit() #save changes

#db.close()  #close database
#command = ""          # test SQL stmt in sqlite3 shell, save as string
#c.execute(command)    # run SQL statement


# Tests
print(get_users())