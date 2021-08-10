from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_family, model_category, model_post, model_img

@app.route('/')
def index():
    if 'uuid' not in session:
        return redirect('/adventure_awaits')
    return redirect('/dashboard')

@app.route('/<string:family_name>')
def onlooker_dashboard(family_name):
    session['page'] = 'onlooker_dashboard'
    print(family_name)
    context = {
        "family": model_family.Family.get_one_by_name(family_name)
    }
    
    return render_template('/onlooker/main.html', **context)

@app.route('/adventure_awaits')
def adventure_awaits():
    session['page'] = 'adventure_awaits'
    context = {
        "all_families": model_family.Family.get_all()
    }
    return render_template('onlooker/landing_page.html', **context)

@app.route('/<string:family_name>/category/<int:category_id>')
def onlooker_category_show(family_name, category_id):
    session['page'] = 'onlooker_one_category'
    context = {
        "family": model_family.Family.get_one_by_name(family_name),
        "category": model_category.Category.get_one(category_id)
    }
    return render_template('onlooker/category_show.html', **context)

@app.route('/<string:family_name>/post/<int:post_id>')
def onlooker_post_show(family_name, post_id):
    session['page'] = 'onlooker_one_post'
    context = {
        "family": model_family.Family.get_one_by_name(family_name),
        "post": model_post.Post.get_one(post_id),
        'images': model_img.Image.get_all_linked(post_id),
    }
    return render_template('onlooker/post_show.html', **context)
