from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash 
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User: 
    db = 'privateWall'
    def __init__(self,data): 
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    
    @staticmethod
    def validate(user):
        isValid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(User.db).query_db(query,user)
        print(results)
        if len(results) >= 1:
            isValid = False
            flash("That email is already taken!", "register")
        if not EMAIL_REGEX.match(user['email']):
            isValid = False
            flash("Invalid email format.", "register")
        if len(user['firstName']) < 2:
            isValid = False
            flash('First name must be at least 2 characters long.', "register")
        if len(user['lastName']) < 2:
            isValid = False
            flash('Last name must be at least 2 characters long.', "register")
        if len(user['password']) < 8:
            isValid = False
            flash('Password must be at least 8 characters long', "register")
        if re.search('[0-9]',user['password']) is None:
            isValid = False
            flash("Password is missing a number.", "register")
        if re.search('[A-Z]',user['password']) is None: 
            isValid = False
            flash("Password is missing a capital letter.", "register")
        if user['password'] != user['confirm']:
            isValid = False
            flash('Passwords do not match', "register")
        return isValid
    
    @classmethod
    def getAll(cls): 
        query = 'SELECT * FROM users;' 
        results = connectToMySQL(cls.db).query_db(query) 
        users = [] 
        for u in results: 
            users.append(cls(u))
        return users 
    
    @classmethod 
    def getOne(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;' 
        results = connectToMySQL(cls.db).query_db(query, data) 
        if len(results) < 1: 
            return False 
        return cls(results[0]) 
        
    
    @classmethod 
    def getEmail(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;' 
        results = connectToMySQL(cls.db).query_db(query, data) 
        if len(results) < 1: 
            return False 
        return cls(results[0]) 
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( firstName , lastName , email , password, createdAt, updatedAt ) VALUES ( %(firstName)s , %(lastName)s , %(email)s , %(password)s, NOW() , NOW() );"
        return connectToMySQL(cls.db).query_db( query, data )


    

    