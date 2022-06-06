from . import bp as app
from flask import render_template,request,redirect,url_for

@app.get('/login')
def login_view():
    return render_template('Login.html')