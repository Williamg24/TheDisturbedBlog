import sqlite3

DB_FILE="user.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

db.execute("DROP TABLE if exists usernames")
c.execute("CREATE TABLE usernames(user TEXT, pass TEXT)")

#check if username in table:
def in_table(username):
    user_list = list(c.execute("SELECT user FROM usernames").fetchall())
    print(user_list)
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



#command = ""          # test SQL stmt in sqlite3 shell, save as string
#c.execute(command)    # run SQL statement



db.commit() #save changes
#db.close()  #close database




# Tests
add_to_db("DWM","ABC") # added to table
print(in_table("DWM")) #true
print(in_table("MARC")) #false
add_to_db("DWM","123") #shouldn't be added