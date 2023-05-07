# import the function that will return an instance of a connection
from flask_app.configs.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    DB = 'user_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
# Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
# make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
    # Create an empty list to append our instances of friends
        users = []
    # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email  ) VALUES ( %(first_name)s , %(last_name)s , %(email)s );"
        # data is a dictionary that will be passed into the save method from server.py
        # return a id for the newly created record
        new_id= connectToMySQL(cls.DB).query_db( query, data )
        return new_id
    # the get_one method will be used when we need to retrieve just one specific row of the table
    @classmethod
    def get_one(cls, user_id):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id':user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    

    @classmethod
    def update(cls,data):
        query = """UPDATE users 
                SET first_name=%(first_name)s,
                last_name=%(last_name)s,email=%(email)s 
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def delete(cls, user_id):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        data = {"id": user_id}
        return connectToMySQL(cls.DB).query_db(query, data)
            
    @staticmethod
    def is_valid_user(user):
        is_valid = True

        if len(user["first_name"]) <= 0:
            is_valid = False
            flash("First name is required.")
        if len(user["last_name"]) <= 0:
            is_valid = False
            flash("Last name is required.")
        if len(user["email"]) <= 0:
            is_valid = False
            flash("Email is required.")

        if len(user["email"]) > 0 and not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email format.")
            is_valid = False

        return is_valid
            
