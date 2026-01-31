import sqlite3
from datetime import date

DB_NAME = "academicTracker.db"

def createDb():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    # print(cursor)

    cursor.execute('CREATE TABLE IF NOT EXISTS dailyLogs (date TEXT PRIMARY KEY,seconds INTEGER DEFAULT 0)')
    connection.commit()
    connection.close()

def addTime(second=1):
    today = str(date.today())

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('INSERT OR IGNORE INTO dailyLogs (date, seconds) VALUES (?, 0)', (today,))
    cursor.execute('UPDATE dailyLogs SET seconds = seconds + ? WHERE date = ?', (second, today))

    connection.commit()
    connection.close()

def fetchTime():
    today = str(date.today())

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('SELECT seconds FROM dailyLogs WHERE date = ?', (today,))
    result = cursor.fetchone()

    connection.close()
    return result[0] if result else 0

createDb()