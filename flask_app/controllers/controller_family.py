from flask_app import app, login_required
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_family

import random
import string

# @app.route('/family/new')
# def new_family():
#     return 'new family'

@app.route('/family/create', methods=['post'])
@login_required
def create_family():
    is_valid = model_family.Family.validate_family(request.form)
    
    if not is_valid:
        flash("Family is not valid")
        return redirect('/')
    
    # Creates the family code of 7 characters
    chars = string.ascii_letters + string.digits
    code = ''.join(random.choice(chars) for _ in range(7))

    data = {
        **request.form,
        "code": code
    }
    family_id = model_family.Family.create(data)

    data = {
        "family_id": family_id,
        "user_id": session['uuid']
    }

    model_family.Family.join(data)

    return redirect('/')

@app.route('/family/join', methods=['POST'])
@login_required
def join_family():
    family = model_family.Family.get_one_by_code(request.form['family_code'])
    print("*"*80)
    print(family)
    data = {
        "user_id": session['uuid'],
        "family_id": family.id
    }
    model_family.Family.join(data)
    return redirect('/')

@app.route('/family/<int:family_id>/leave')
@login_required
def leave_family(family_id):
    data = {
        "family_id": family_id,
        "user_id": session['uuid']
    }
    model_family.Family.leave_family(data)
    return redirect('/')

# TODO: Finish family CRUD - controller
# @app.route('/family/<int:id>')
# def show_family(id):
#     return 'show family'

# @app.route('/family/<int:id>/edit')
# def edit_family(id):
#     return 'edit family'

# @app.route('/family/<int:id>/update', methods=['post'])
# def update_family(id):
#     return 'update family'

# @app.route('/family/<int:id>/delete')
# def delete_family(id):
#     return 'delete family'