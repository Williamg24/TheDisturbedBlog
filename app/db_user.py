import sqlite3

DB_FILE="user.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

c.execute("CREATE TABLE usernames(user TEXT, pass TEXT")
db_values = c.execute("SELECT * FROM usernames").fetchall()

#check if username in table:
def in_table(username):
    user_list = list(db_values)
    print(user_list) 
    return username in user_list 

#adds new username and password to table if not exist
def add_to_db(username,password):
    if in_table(username): 
        return "Username already exists"
    else:
        c.excute(f'"INSERT INTO usernames VALUES("{username}","{password}")"')
    db.commit()
    print(db_values) 



#command = ""          # test SQL stmt in sqlite3 shell, save as string
#c.execute(command)    # run SQL statement



db.commit() #save changes
db.close()  #close database