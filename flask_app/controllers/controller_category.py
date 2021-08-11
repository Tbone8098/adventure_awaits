from flask_app import app, login_required
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_category, model_user

# @app.route('/category/new')
# def new_category():
#     return 'new category'

@app.route('/category/create', methods=['post'])
@login_required
def create_category():
    is_valid = model_category.Category.validate_category(request.form)

    if not is_valid:
        return redirect('/settings')
    
    if not model_user.User.get_one(session['uuid']).get_family:
        flash("You must join or create a family first")
        return redirect('/settings')

    info = {
        **request.form,
        "family_id": model_user.User.get_one(session['uuid']).get_family.id
    }

    model_category.Category.create(info)
    return redirect('/settings')

@app.route('/category/<int:id>')
@login_required
def show_category(id):
    category = model_category.Category.get_one(id)
    session['page'] = f'{category.name} Category'
    context = {
        "category": category
    }
    return render_template('admin/pages/category_show.html', **context)

# TODO: Finish Category CRUD - controller
# @app.route('/category/<int:id>/edit')
# def edit_category(id):
#     return 'edit category'

# @app.route('/category/<int:id>/update', methods=['post'])
# def update_category(id):
#     return 'update category'

# @app.route('/category/<int:id>/delete')
# def delete_category(id):
#     return 'delete category'