from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

DATABASE_SCHEMA = 'adventure_awaits_2_db'

class Image:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.base64 = data['base64']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# C !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def create(cls, info):
        query = 'INSERT INTO images (base64, title) VALUES (%(base64)s, %(title)s)'
        data = {
            'base64' : info['base64'],
            'title' : info['title'],
        }

        new_images_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

        return new_images_id
    
    @classmethod
    def create_image_link(cls, info):
        query = 'INSERT INTO posts_has_images (post_id, image_id) VALUES (%(post_id)s, %(image_id)s)'
        data = {
            'post_id' : info['post_id'],
            'image_id' : info['image_id'],
        }

        return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
    
# R !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM images;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if len(results) > 0:
            all_images = []
            for images in results:
                all_images.append(cls(images))
            return all_images

    @classmethod
    def get_all_linked(cls, post_id):
        query = 'SELECT * FROM posts_has_images JOIN images ON images.id = image_id WHERE post_id = %(post_id)s;'
        data = {
            'post_id': post_id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        print(results)
        if results:
            all_images = []
            for image in results:
                all_images.append(Image.get_one(image['id']))
            return all_images
        return results
        

    @classmethod
    def get_one(cls, id):
        query = 'SELECT * FROM images WHERE id = %(id)s;'
        data = {
            'id': id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        one_images = []
        if len(results) > 0:
           return cls(results[0])
        return results
    
# U !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def update_one(cls, info):
        # TODO: add the ability to update pw 
        query = 'UPDATE images SET link=%(link)s WHERE id=%(id)s'
        data = {
            'link': info['link'],
            'id': info['id'],
        }
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

# D !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def delete_one(cls, id):
        query = 'DELETE FROM images WHERE id=%(id)s'
        data = {
            'id': id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return id


# ******************************************* VALIDATIONS ********************************************
    @staticmethod
    def validate_images(user_data):
        is_valid = True

        if len(user_data['title']) < 3: 
            is_valid = False
            flash('Title name must be greater than 3 characters')

        if len(user_data['base64']) < 3: 
            is_valid = False
            flash('Must pick a image to upload')
        
        return is_valid