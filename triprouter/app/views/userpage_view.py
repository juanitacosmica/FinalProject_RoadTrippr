from . import bp as app
from flask import render_template

@app.get('/userpage')
def userpage_view():
    return render_template('userpage.html')