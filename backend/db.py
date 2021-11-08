import json, mysql.connector

class db:
    def __init__(self):
        config = json.load(open('backend/private.json'))
        self.mydb = mysql.connector.connect(
            host = config['host'],
            user = config['user'],
            passwd = config['password'],
            database = config['database']
            )
        # preparing a cursor object
        self.cursor = self.mydb.cursor()

    def validate(self, username: str, password: str):
        query = "SELECT COUNT(*) FROM user WHERE username=%s AND password=%s;"
        values = (username, password)
        self.cursor.execute(query, values)
        count = self.cursor.fetchone()[0]
        if count == 1:
            return True
        else:
            return False
    
    def get_duplicates(self, username: str, email: str):
        query = "SELECT COUNT(*) FROM user WHERE username=%s OR email=%s;"
        values = (username, email)
        self.cursor.execute(query, values)
        count = self.cursor.fetchone()[0]
        if count >= 1:
            return True
        else:
            return False

    def create_account(self, username: str, password: str, first: str, last: str, email: str):
        query = "INSERT INTO user VALUES(%s, %s, %s, %s, %s);"
        values = (username, password, first, last, email)
        self.cursor.execute(query, values)
        self.cursor.fetchone()
        self.mydb.commit()
    
    def reset(self):
        f = open('backend/resetDB.sql', 'r').read().split('\n')
        for query in f:
            self.cursor.execute(query)
        self.mydb.commit()
    
    def close(self):
        self.mydb.close()