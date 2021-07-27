from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_user

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# @app.route('/user/new')
# def new_user():
#     return 'new user'

@app.route('/user/create', methods=['post'])
def create_user():
    is_valid = model_user.User.validate_user(request.form)

    if not is_valid:
        return redirect('/register')

    hash_pw = bcrypt.generate_password_hash(request.form['pw'])
    
    info = {
        **request.form,
        "hash_pw": hash_pw
    }
    user_id = model_user.User.create(info)
    session['uuid'] = user_id
    return redirect('/')

# TODO: Finish user CRUD - controller
# @app.route('/user/<int:id>')
# def show_user(id):
#     return 'show user'

# @app.route('/user/<int:id>/edit')
# def edit_user(id):
#     return 'edit user'

# @app.route('/user/<int:id>/update', methods=['post'])
# def update_user(id):
#     return 'update user'

# @app.route('/user/<int:id>/delete')
# def delete_user(id):
#     return 'delete user'