from . import bp as app
from flask import render_template,request,redirect,url_for

@app.get('/navigation')
def navigation_view():
    return render_template('navigation.html')