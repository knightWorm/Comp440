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
        query = "SELECT COUNT(*) FROM users WHERE username=%s AND password=%s;"
        values = (username, password)
        self.cursor.execute(query, values)
        count = self.cursor.fetchone()[0]
        if count == 1:
            return True
        else:
            return False
    
    def get_duplicates(self, username: str, email: str):
        query = "SELECT COUNT(*) FROM users WHERE username=%s OR email=%s;"
        values = (username, email)
        self.cursor.execute(query, values)
        count = self.cursor.fetchone()[0]
        if count >= 1:
            return True
        else:
            return False

    def create_account(self, username: str, password: str, first: str, last: str, email: str):
        query = "INSERT INTO users VALUES(%s, %s, %s, %s, %s);"
        values = (username, password, first, last, email)
        self.cursor.execute(query, values)
        self.cursor.fetchone()
        self.mydb.commit()
    
    def create_blog(self, subject: str, description: str, tags:str, created_by:str):
        # Insert blog
        query = "INSERT INTO blogs VALUES(NULL, %s, %s, CURDATE(), %s);"
        values = (subject, description, created_by)
        self.cursor.execute(query, values)
        # Insert tags
        tags = [tag.strip() for tag in tags.split(',')]
        for tag in tags:
            query = "INSERT INTO blogstags VALUES((SELECT MAX(blogid) FROM blogs), %s);"
            values = (tag,)
            self.cursor.execute(query, values)
        self.mydb.commit()
    
    def reset(self):
        f = open('backend/ProjDB.sql', 'r').read()
        self.cursor.execute(f, multi=True)
    
    def close(self):
        self.mydb.close()