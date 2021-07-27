from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_user, model_post

@app.route('/post/new')
def new_post():
    session['page'] = 'post_new'
    context = {
        "user": model_user.User.get_one(session['uuid'])
    }
    return render_template('admin/pages/post_new.html', **context)

@app.route('/post/create', methods=['post'])
def create_post():
    is_valid = model_post.Post.validate_posts(request.form)

    if not is_valid:
        return redirect('/post/new')

    user = model_user.User.get_one(session['uuid'])
    family = user.get_family
    family_id = family.id

    info = {
        **request.form, 
        'author_id': session['uuid'],
        'family_id': family_id
    }

    print(info)

    model_post.Post.create(info)

    return redirect('/')

@app.route('/post/<int:id>')
def show_post(id):
    session['page'] = 'show_post'
    context = {
        'user': model_user.User.get_one(session['uuid']),
        'post': model_post.Post.get_one(id)
    }
    return render_template('admin/pages/post_show.html', **context)

# TODO: Finish Post CRUD - controller
# @app.route('/post/<int:id>/edit')
# def edit_post(id):
#     return 'edit post'

# @app.route('/post/<int:id>/update', methods=['post'])
# def update_post(id):
#     return 'update post'

# @app.route('/post/<int:id>/delete')
# def delete_post(id):
#     return 'delete post'