from flask_app import app, login_required
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_user, model_post, model_img

@app.route('/post/new')
@login_required
def new_post():
    session['page'] = 'post_new'
    context = {
        "user": model_user.User.get_one(session['uuid']),
        "post": ""
    }
    return render_template('admin/pages/post_new.html', **context)

@app.route('/post/create', methods=['post'])
@login_required
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

    if 'is_public' in request.form:
        info['is_public'] = 1
    else:
        info['is_public'] = 0

    print(info)

    model_post.Post.create(info)

    return redirect('/blogs')

@app.route('/post/<int:id>')
@login_required
def show_post(id):
    session['page'] = 'show_post'
    context = {
        'user': model_user.User.get_one(session['uuid']),
        'post': model_post.Post.get_one(id),
        'images': model_img.Image.get_all_linked(id)
    }
    return render_template('admin/pages/post_show.html', **context)

@app.route('/post/<int:id>/edit')
def edit_post(id):
    context = {
        'user': model_user.User.get_one(session['uuid']),
        'post': model_post.Post.get_one(id),
        'all_images': model_img.Image.get_all(),
    }
    return render_template('admin/pages/post_new.html', **context)

@app.route('/post/<int:id>/update', methods=['post'])
def update_post(id):
    info = {
        **request.form,
        'id': id
    }
    if 'is_public' in request.form:
        info['is_public'] = 1
    else:
        info['is_public'] = 0
    
    model_post.Post.update_one(info)

    return redirect('/blogs')

# AJAX Call
@app.route('/post/<int:post_id>/update_public/<status>')
def update_public(post_id, status):
    msg = "success"
    print(f"status: {status}")
    if status == 'true':
        status = 1
    else:
        status = 0
    model_post.Post.update_public(post_id, status)
    return jsonify(msg)

@app.route('/post/<int:id>/delete')
def delete_post(id):
    model_post.Post.delete_one(id)
    return redirect('/blogs')



# ***************** Blogs Section *************************

@app.route('/blogs')
@login_required
def blog_dashboard():
    session['page'] = 'Blog Dashboard'
    context = {
        'user': model_user.User.get_one(session['uuid']),

    }

    return render_template('admin/pages/blogs.html', **context)

@app.route('/blog/filter', methods=['POST'])
def filter_blogs():
    
    return redirect('/blogs')

