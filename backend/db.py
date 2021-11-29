import json, mysql.connector

class db:
    def __init__(self):
        config = json.load(open('backend/private.json'))
        self.mydb = mysql.connector.connect(
            host = config['host'],
            port = config['port'],
            user = config['user'],
            passwd = config['password'],
            database = config['database']
            )
        # preparing a cursor object
        self.cursor = self.mydb.cursor()

    def validate(self, username:str, password:str):
        query = "SELECT COUNT(*) FROM users WHERE username=%s AND password=%s;"
        values = (username, password)
        self.cursor.execute(query, values)
        count = self.cursor.fetchone()[0]
        if count == 1:
            return True
        else:
            return False
    
    def get_duplicates(self, username:str, email:str):
        query = "SELECT COUNT(*) FROM users WHERE username=%s OR email=%s;"
        values = (username, email)
        self.cursor.execute(query, values)
        count = self.cursor.fetchone()[0]
        if count >= 1:
            return True
        else:
            return False

    def create_account(self, username:str, password:str, first:str, last:str, email:str):
        query = "INSERT INTO users VALUES(%s, %s, %s, %s, %s);"
        values = (username, password, first, last, email)
        self.cursor.execute(query, values)
        self.cursor.fetchone()
        self.mydb.commit()
    
    def create_blog(self, subject:str, description:str, tags:str, created_by:str):
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

    def create_comment(self, sentiment:int, description:str, blogid:str, posted_by:str):
        query = "INSERT INTO comments VALUES(NULL, %s, %s, CURDATE(), %s, %s);"
        values = (sentiment, description, blogid, posted_by)
        self.cursor.execute(query, values)
        self.mydb.commit()
    
    def get_options(self):
        query = "SELECT blogid, subject FROM blogs;"
        self.cursor.execute(query)
        options = ""
        for (blogid, subject) in self.cursor:
            options += "<option value='{}'>{}</option>".format(blogid, subject)
        return options

    def get_blog(self, blogid):
        query = "SELECT subject, created_by, description FROM blogs WHERE blogid=%s;"
        self.cursor.execute(query, (blogid,))
        blg = self.cursor.fetchone()
        query = "SELECT tag FROM blogstags WHERE blogid=%s;"
        self.cursor.execute(query, (blogid,))
        tags = ""
        for tag in self.cursor.fetchall():
            tags += tag[0] + ", "
        post = "{} from {} \n\n{}\n\nTags: {}".format(blg[0], blg[1], blg[2], tags[:-2])
        return post
    
    def get_comments(self, blogid):
        query = "SELECT posted_by, sentiment, description FROM comments WHERE blogid=%s;"
        self.cursor.execute(query, (blogid,))
        post = ""
        for (posted_by, sentiment, description) in self.cursor:
            emoji = "👎"
            if sentiment == "positive":
                emoji = "👍"
            post += "\n{} {}\n{}".format(posted_by, emoji, description)
        return post

    def reset(self):
        f = open('backend/ProjDB.sql', 'r').read()
        self.cursor.execute(f, multi=True)
    
    def close(self):
        self.mydb.close()