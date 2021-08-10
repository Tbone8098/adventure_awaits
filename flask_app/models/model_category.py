from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

from flask_app.models import model_post

DATABASE_SCHEMA = 'adventure_awaits_2_db'

class Category:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.family_id = data['family_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @property
    def get_all_posts(self):
        query = 'SELECT id FROM posts WHERE category_id = %(cat_id)s'
        data = {
            "cat_id": self.id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results):
            all_posts = []
            for post in results:
                all_posts.append(model_post.Post.get_one(post['id']))
            return all_posts
        return results

    @property
    def count_public(self):
        results = self.get_all_posts
        if results:
            count = 0
            for post in results:
                if post.is_public == True:
                    count += 1
            return count
        return results

# C
    @classmethod
    def create(cls, info):
        query = "INSERT INTO categories (name, description, family_id) VALUES (%(name)s, %(description)s, %(family_id)s)"
        data = {
            "name" : info['name'],
            "description" : info['description'],
            "family_id" : info['family_id'],
        }

        new_categories_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

        return new_categories_id
    
# R
    @classmethod
    def get_all(cls, family_id):
        query = 'SELECT * FROM categories WHERE family_id = %(family_id)s;'
        data = {
            "family_id": family_id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        all_categories = []
        if len(results) > 0:
            for page in results:
                all_categories.append(cls(page))
        return all_categories

    @classmethod
    def get_one(cls, id):
        query = 'SELECT * FROM categories WHERE id = %(category_id)s;'
        data = {
            "category_id": id
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        return result
    
# U
    @classmethod
    def update_one(cls, info):
        # TODO: add the ability to update pw 
        query = 'UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, hash_pw=%(hash_pw)s WHERE id=%(id)s'
        data = {
            "first_name": info['first_name'],
            "last_name": info['last_name'],
            "email": info['email'],
            "hash_pw": info['hash_pw'],
            "id": info['id'],
        }
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

# D
    @classmethod
    def delete_one(cls, id):
        query = 'DELETE FROM users WHERE id=%(id)s'
        data = {
            "id": id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        print(f"user with the id {id} has been deleted")
        return id

    # Delete if not a user model
    @staticmethod
    def validate_category(user_data):
        is_valid = True

        if len(user_data['name']) < 3: 
            is_valid = False
            flash("Page name must be greater than 3 characters")

        if len(user_data['description']) < 3: 
            is_valid = False
            flash("Description must be greater than 3 characters")

        
        return is_valid