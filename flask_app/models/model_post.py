from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

DATABASE_SCHEMA = 'adventure_awaits_2_db'

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.author_id = data['author_id']
        self.category_id = data['category_id']
        self.family_id = data['family_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# C !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def create(cls, info):
        query = 'INSERT INTO posts (title, content, author_id, category_id, family_id) VALUES (%(title)s, %(content)s, %(author_id)s, %(category_id)s, %(family_id)s)'
        data = {
            'title' : info['title'],
            'content' : info['content'],
            'author_id' : info['author_id'],
            'category_id' : info['category_id'],
            'family_id' : info['family_id'],
        }

        new_posts_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

        return new_posts_id
    
# R !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM posts;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if len(results) > 0:
            all_posts = []
            for posts in results:
                all_posts.append(cls(posts))
            return all_posts

    @classmethod
    def get_one(cls, post_id):
        query = 'SELECT * FROM posts WHERE id = %(post_id)s;'
        data = {
            'post_id': post_id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results) > 0:
           return cls(results[0])
        return results
    
# U !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def update_one(cls, info):
        # TODO: add the ability to update pw 
        query = 'UPDATE posts SET title=%(title)s WHERE id=%(title_id)s'
        data = {
            'first_name': info['first_name'],
            'title_id': info['id'],
        }
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

# D !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def delete_one(cls, title_id):
        query = 'DELETE FROM posts WHERE id=%(title_id)s'
        data = {
            'titleid': title_id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return id


# ******************************************* VALIDATIONS ********************************************
    @staticmethod
    def validate_posts(user_data):
        is_valid = True

        if len(user_data['title']) < 3: 
            is_valid = False
            flash('title name must be greater than 3 characters')
        
        return is_valid