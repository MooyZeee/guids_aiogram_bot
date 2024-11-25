import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# telegram_id, username, first_name, last_name, enter_name, number
def createTableDatabase():
    #players list
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        playerId integer primary key,
        telegramId integer,
        telegramUserName varchar(50),
        firstName varchar(50),
        lastName varchar(50) default 'None')
    """)
    # admins list
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
        playerId integer primary key,
        telegramId integer,
        telegramUserName varchar(50),
        firstName varchar(50),
        lastName varchar(50) default 'None')
    """)
    conn.commit()

def insertInfoUsersDatabase(telegram_id, username, first_name, last_name):
    cur.execute("""
    INSERT INTO users (telegramId, telegramUserName, firstName, lastName)
    VALUES 
    (?, ?, ?, ?)
    """, (telegram_id, username, first_name, last_name))
    conn.commit()

def insertInfoAdminsDatabase(telegram_id, username, first_name, last_name):
    cur.execute("""
    INSERT INTO admins (telegramId, telegramUserName, firstName, lastName)
    VALUES 
    (?, ?, ?, ?)
    """, (telegram_id, username, first_name, last_name))
    conn.commit()
    conn.close()

def selectInfoUsersDatabase():
    cur.execute("""SELECT telegramId, telegramUserName, firstName, lastName FROM users""")

def selectInfoAdminsDatabase():
    cur.execute("""SELECT telegramId, telegramUserName, firstName, lastName FROM admins""")





# createTableDatabase()
# insertInfoIdDatabase(345634567876543, 'mooyzeee', 'Mov', 'Coder')


