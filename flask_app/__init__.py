from functools import wraps
from flask import Flask, render_template, redirect, request, session, flash, jsonify
app = Flask(__name__)
app.secret_key = 'Whos your daddy? Goons your daddy!'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'uuid' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect('/')

    return wrap