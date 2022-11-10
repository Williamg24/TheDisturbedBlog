import sqlite3

DB_FILE="user.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

db.execute("DROP TABLE if exists usernames")
db.execute("DROP TABLE if exists main")
c.execute("CREATE TABLE usernames(user TEXT UNIQUE, pass TEXT)")
c.execute("CREATE TABLE main(user TEXT UNIQUE, title TEXT, content TEXT, date_added INTEGER, data_mod INTEGER, num_view INTEGER, time INTEGER)")

#check if username in table: (helper function)
def in_table(username):
    user_list = list(c.execute("SELECT user FROM usernames").fetchall())
    #print(user_list)
    for i in user_list:
        for j in i:
            return username == j
    return False

#adds new username and password to table if not exist
def add_to_db(username,password):
    if in_table(username): 
        return False
    else:
        c.execute(f'INSERT INTO usernames VALUES("{username}","{password}")')
    db.commit() 

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


db.commit() #save changes

#db.close()  #close database
#command = ""          # test SQL stmt in sqlite3 shell, save as string
#c.execute(command)    # run SQL statement


# Tests
add_to_db("DWM","ABC") # added to table
print(in_table("DWM")) #true
print(in_table("MARC")) #false
add_to_db("DWM","123") #shouldn't be added
print(c.execute("SELECT * FROM usernames").fetchall())
print("Password of 'DWM' is "+ get_pass("DWM")) # return ABC
print(correct_pass("DWM","123")) # should be false