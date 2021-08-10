from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_user, model_category, model_post
import re

DATABASE_SCHEMA = 'adventure_awaits_2_db'

class Family:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.code = data['code']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @property
    def get_all_categories(self):
        query = 'SELECT id FROM categories WHERE family_id = %(family_id)s;'
        data = {
            'family_id': self.id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results):
            all_categories = []
            for cat in results:
                all_categories.append(model_category.Category.get_one(cat['id']))
            return all_categories
        return False

    @property
    def get_all_posts(self):
        query = "SELECT id FROM posts WHERE family_id = %(family_id)s ORDER BY created_at desc"
        data = {
            'family_id': self.id,
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if results:
            all_posts = []
            for post in results:
                all_posts.append(model_post.Post.get_one(post['id']))
            return all_posts
        return results


    def get_categories(self):
        query ='SELECT categories.id FROM categories WHERE family_id = %(family_id)s;'
        data = {
            "family_id": self.id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if results != False:
            all_pages = []
            for page in results:
                all_pages.append(model_category.Category.get_one(page['id']))
            return all_pages
        return []


    def get_members(self):
        query = 'SELECT users.id FROM users_has_families JOIN users ON user_id = users.id WHERE family_id = %(id)s'
        data = {
            "id": self.id
        }
        results =  connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results) > 0:
            user_list = []
            for user_id in results:
                user_list.append(model_user.User.get_one(user_id['id']))
            return user_list
        return results

# C
    @classmethod
    def create(cls, info):
        query = "INSERT INTO families (name, code) VALUES (%(name)s, %(code)s)"
        data = {
            "name" : info['name'],
            "code": info['code']
        }

        new_families_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

        return new_families_id

    @classmethod
    def join(cls, data):
        query = 'INSERT INTO users_has_families (user_id, family_id) VALUES (%(user_id)s, %(family_id)s)'
        return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
    
# R
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM families;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        all_families = []
        for family in results:
            all_families.append(cls(family))
        return all_families

    @classmethod
    def get_one(cls, id):
        query = 'SELECT * FROM families WHERE id = %(family_id)s;'
        data = {
            "family_id": id
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(result) > 0:
            return cls(result)
        return result

    @classmethod
    def get_users_family(cls,user_id):
        query = 'SELECT * FROM users_has_families JOIN families ON family_id = families.id WHERE user_id = %(user_id)s'
        data = {
            "user_id": user_id
        }
        family = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        if len(family) > 0:
            family = cls(family[0])
        return family

    @classmethod
    def get_one_by_code(cls, code):
        query = 'SELECT * FROM families WHERE code = %(family_code)s;'
        data = {
            "family_code": code
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        return result

    @classmethod
    def get_one_by_name(cls, family_name):
        query = 'SELECT * FROM families WHERE name = %(family_name)s;'
        data = {
            "family_name": family_name
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        return result

    
# U
    @classmethod
    def update_one(cls, info):
        # TODO: add the ability to update pw 
        query = 'UPDATE families SET name=%(name)s WHERE id=%(id)s'
        data = {
            "first_name": info['first_name'],
        }
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)


# D
    @classmethod
    def delete_one(cls, id):
        query = 'DELETE FROM families WHERE id=%(id)s'
        data = {
            "id": id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return id

    @classmethod
    def leave_family(cls, data):
        query = 'DELETE FROM users_has_families WHERE family_id = %(family_id)s AND user_id = %(user_id)s'
        return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

    # Delete if not a user model
    @staticmethod
    def validate_family(data):
        is_valid = True

        return is_valid