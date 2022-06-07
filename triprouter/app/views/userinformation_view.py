from . import bp as app
from flask import render_template,request,redirect,url_for

@app.get('/userinformation')
def userinformation_view():
    return render_template('userinformation.html')