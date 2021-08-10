from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_category
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
        self.date = data['date']
        self.time = data['time']
        self.ampm = data['ampm']
        self.is_public = data['is_public']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @property
    def category(self):
        return model_category.Category.get_one(self.category_id)

# C !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def create(cls, info):
        query = 'INSERT INTO posts (title, content, author_id, category_id, family_id, is_public) VALUES (%(title)s, %(content)s, %(author_id)s, %(category_id)s, %(family_id)s, %(is_public)s)'
        data = {
            'title' : info['title'],
            'content' : info['content'],
            'author_id' : info['author_id'],
            'category_id' : info['category_id'],
            'family_id' : info['family_id'],
            'is_public' : info['is_public'],
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
        query = "SELECT *, DATE_FORMAT(created_at, '%%%%Y-%%%%m-%%%%d') as date,  DATE_FORMAT(created_at, '%%%%h %%%%i') as time,  DATE_FORMAT(created_at, '%%%%p') as ampm FROM posts WHERE id = %(post_id)s;"
        data = {
            'post_id': post_id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results) > 0:
           return cls(results[0])
        return results

    @classmethod
    def get_one_filter(cls, data):
        query = 'SELECT %(categories)s FROM posts WHERE %(condition)s;'

        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return results
    
# U !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def update_one(cls, info):
        # TODO: add the ability to update pw 
        query = 'UPDATE posts SET title=%(title)s, content=%(content)s, category_id=%(category_id)s, is_public=%(is_public)s WHERE id=%(id)s'
        data = {
            'title': info['title'],
            'content': info['content'],
            'category_id': info['category_id'],
            'is_public': info['is_public'],
            'id': info['id'],
        }
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

    @classmethod
    def update_public(cls, post_id, status):
        query = 'UPDATE posts SET is_public = %(status)s WHERE id = %(post_id)s'
        data = {
            'status': status,
            'post_id': post_id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

# D !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def delete_one(cls, id):
        query = 'DELETE FROM posts WHERE id=%(id)s'
        data = {
            'id': id
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