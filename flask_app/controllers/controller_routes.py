from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_family

@app.route('/')
def index():
    if 'uuid' not in session:
        return redirect('/main')
    return redirect('/dashboard')

@app.route('/<string:family_name>')
def family_page(family_name):
    session['page'] = f'The {family_name}'
    context = {
        "family": model_family.Family.get_one_by_name(family_name)
    }
    
    return render_template('/onlooker/landing_page.html', **context)

@app.route('/main')
def main():
    context = {
        "all_families": model_family.Family.get_all()
    }
    return render_template('onlooker/main.html', **context)