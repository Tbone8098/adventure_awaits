from flask_app import app, login_required
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_user

@app.route('/login')
def admin_login():
    session['page'] = 'login'
    return render_template('/admin/pages/login.html')

@app.route('/process_login', methods=['POST'])
def admin_process_login():

    user = model_user.User.get_one_by_email(request.form['login'])

    if len(user) < 1:
        print("no email")
        user = model_user.User.get_one_by_username(request.form['login'])
        if len(user) < 1:
            print('no username')
            flash("No user found")
            return redirect('/login')
    
    session['uuid'] = user[0]['id']
    return redirect('/')

@app.route('/register')
def admin_register():
    session['page'] = 'register'
    return render_template('/admin/pages/register.html')

@app.route('/logout')
def admin_logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
@login_required
def admin_dashboard():
    session['page'] = 'dashboard'
    context = {
        "user": model_user.User.get_one(session['uuid'])
    }
    return render_template('/admin/pages/dashboard.html', **context)

@app.route('/settings')
@login_required
def admin_settings():
    session['page'] = 'settings'
    context = {
        "user": model_user.User.get_one(session['uuid'])
    }
    return render_template('/admin/pages/settings.html', **context)