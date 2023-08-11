import sqlite3

def createDatabase(dir):
    conn = None
    try:
        conn = sqlite3.connect(f"{dir}/tracking.db")
    except sqlite3.Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute(''' CREATE TABLE IF NOT EXISTS detections ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [longitude] REAL, [latitude] REAL, [path] TEXT, [time] TEXT, [date] TEXT) ''')
    conn.commit()
    return cur.lastrowid

def createConnection(dir):
    conn = None
    try:
        conn = sqlite3.connect(f"{dir}/tracking.db")
    except sqlite3.Error as e:
        print(e)
    return conn

def commitDetection(conn, detection):
    sqlCommit = ''' INSERT INTO detections(longitude, latitude, path, time, date) VALUES(?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sqlCommit, detection)
    conn.commit()
    return cur.lastrowid

def queryTable(conn, table):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    for row in rows:
        print(row)