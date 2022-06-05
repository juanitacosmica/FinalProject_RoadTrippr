from . import bp as app
from flask import render_template,request,redirect,url_for

@app.get('/')
def index_view():
    return render_template('index.html')