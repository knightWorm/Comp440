import json, mysql.connector

class db:
    def __init__(self):
        config = json.load(open('backend/private.json'))
        self.dataBase = mysql.connector.connect(
            host = config['host'],
            user = config['user'],
            passwd = config['password'],
            database = config['database']
            )
        # preparing a cursor object
        self.cursor = self.dataBase.cursor()

    def validate(self, username: str, password: str):
        query = "SELECT COUNT(*) FROM user WHERE username='"+ username +"' AND password='"+ password +"';"
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]
        if count == 1:
            return True
        else:
            return False
    
    def get_users(self):
        query = "SELECT username FROM user;"
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        return users
    
    def close(self):
        self.dataBase.close()