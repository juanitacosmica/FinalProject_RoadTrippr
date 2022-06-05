from . import bp as app
from flask import render_template,request,redirect,url_for

@app.get('/questionaire')
def questionaire_view():
    return render_template('questionaire.html')