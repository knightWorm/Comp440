from datetime import  date
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
    
    def get_active_user_options(self):
        query = "SELECT created_by FROM blogs GROUP BY created_by;"
        self.cursor.execute(query)
        options = ""
        for (created_by,) in self.cursor:
            options += "<option value='{}'>{}</option>".format(created_by, created_by)
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

    def get_positive_blogs(self, username):
        query = "SELECT blogid FROM blogs WHERE created_by=%s;"
        self.cursor.execute(query, (username,))
        blogids = [blogid[0] for blogid in self.cursor.fetchall()]
        positiveBlogs = []
        for blogid in blogids:
            query = "SELECT sentiment FROM comments WHERE blogid=%s;"
            self.cursor.execute(query, (blogid,))
            sentimentList = [sentiment[0] for sentiment in self.cursor.fetchall()]
            positive = True
            for sent in sentimentList:
                if sent == "negative":
                    positive = False
                    break
            if positive and len(sentimentList) > 0:
                positiveBlogs.append(blogid)
        if len(positiveBlogs) == 0:
            return "There are no positive comments"
        post = ""
        for blogid in positiveBlogs:
            post += "\n" + self.get_blog(blogid)
        return post
    
    def get_most_blogs(self, pdate: date):
        # Find the users with the max count of blogs for a day
        query = "SELECT MAX(created_by) FROM blogs WHERE pdate=%s"
        self.cursor.execute(query, (pdate,))
        users = [user[0] for user in self.cursor.fetchall()]
        if users == [None]:
            return "None"
        usersString = ""
        for user in users:
            usersString += user + ", "
        return usersString[:-2]
    
    def get_leadernames(self, userX, userY):
        # List the users who are followed by X and Y
        query = "SELECT leadername FROM follows WHERE followername=%s AND leadername IN (SELECT leadername FROM follows WHERE followername=%s);"
        values = (userX, userY)
        self.cursor.execute(query, values)
        users = [user[0] for user in self.cursor.fetchall()]
        if len(users) == 0:
            return "None"
        usersString = ""
        for user in users:
            usersString += user + ", "
        return usersString[:-2]

    def valid_blog_count(self, created_by):
        query = "SELECT COUNT(*) FROM blogs WHERE created_by=%s AND pdate=CURDATE();"
        self.cursor.execute(query, (created_by,))
        count = self.cursor.fetchone()[0]
        # Users can only make 2 blogs a day
        if count <= 1:
            return True
        else:
            return False
    
    def valid_comment(self, posted_by, blogid):
        # Only one comment per blog
        query = "SELECT COUNT(*) FROM comments WHERE posted_by=%s AND blogid=%s AND cdate=CURDATE();"
        values = (posted_by, blogid)
        self.cursor.execute(query, values)
        count = self.cursor.fetchone()[0]
        if count > 0:
            return False
        # Only 3 comments for a day
        query = "SELECT COUNT(*) FROM comments WHERE posted_by=%s and cdate=CURDATE();"
        self.cursor.execute(query, (posted_by,))
        count = self.cursor.fetchone()[0]
        if count >= 3:
            return False
        # Can't comment on your own blog
        query = "SELECT COUNT(*) FROM blogs WHERE created_by=%s AND blogid=%s;"
        values = (posted_by, blogid)
        self.cursor.execute(query, values)
        count = self.cursor.fetchone()[0]
        if count >= 1:
            return False
        return True

    def reset(self):
        f = open('backend/ProjDB.sql', 'r').read()
        self.cursor.execute(f, multi=True)
    
    def close(self):
        self.mydb.close()

    def get_user_options(self):
        query = "SELECT userid, username FROM users, blogs, comments WHERE users.username = blogs.created_by AND blogs.blogsid = comments.blogid AND comments.sentiment = positive;"
        self.cursor.execute(query)
        options = ""
        for (userid, username) in self.cursor:
            options += "<option value='{}'>{}</option>".format(userid, username)
        return options

    def valid_positive_blogs(self, blogid):
        query = "SELECT subject, created_by, description FROM blogs, comments WHERE blogid=%s AND sentiment=%s;"
        self.cursor.execute(query, (blogid,))
        blg = self.cursor.fetchone()
        query = "SELECT tag FROM blogstags WHERE blogid=%s;"
        self.cursor.execute(query, (blogid,))
        tags = ""
        for tag in self.cursor.fetchall():
            tags += tag[0] + ", "
        post = "{} from {} \n\n{}\n\nTags: {}".format(blg[0], blg[1], blg[2], tags[:-2])
        return post

    def get_most_blogs_(self, pdate):
        #find the max count of blogs for a day and who posted them
        query = "SELECT created_by, MAX(blogCounts) AS max_blogs FROM (SELECT created_by, COUNT(blogid) AS blogCounts FROM blogs WHERE pdate=%s GROUP BY created_by;"
        self.cursor.execute(query, (pdate,))
        post = ""
        for (created_by, max_blogs) in self.cursor:
            post = "\n{}\n{}".format(created_by, max_blogs)
        return post

    def valid_date_blog_count(self, pdate):
        #No blogs exist for date
        query = "SELECT COUNT(*) FROM blogs WHERE pdate=%s"
        values = (pdate)
        self.cursor.execute(query, values)
        count = self.cursor.fetchone()[0]
        if count < 1:
            return False
        return True

    def no_blogs(self):
        query = "SELECT username FROM users LEFT JOIN blogs ON username = created_by WHERE blogid IS NULL;"
        self.cursor.execute(query)
        names = ""
        for (username,) in self.cursor:
            names += username + ", "
        return names[:-2]

    def neg_comments(self):
        query = "SELECT posted_by FROM comments WHERE posted_by NOT IN (SELECT posted_by FROM comments WHERE sentiment = 'positive');"
        self.cursor.execute(query)
        names = ""
        for (posted_by,) in self.cursor:
            names += posted_by + ", "
        return names[:-2]

    def no_neg_comments(self):
        query = "SELECT created_by FROM blogs, (SELECT * FROM comments WHERE blogid NOT IN (SELECT blogid FROM comments WHERE sentiment = 'negative')) AS noNegative WHERE blogs.blogid = noNegative.blogid GROUP BY created_by;"
        self.cursor.execute(query)
        names = ""
        for (created_by,) in self.cursor:
            names += created_by + ", "
        return names[:-2]