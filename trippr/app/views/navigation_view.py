from . import bp as app
import TrippRoller as tr
from flask import render_template,request,redirect,url_for
import json

@app.get('/navigation')
def navigation_view():
    return render_template('navigation.html')

@app.post('/script')
def script_view():
    var = request.form.get('end')
    cluster = request.form.get('cluster')
    value_to_console = tr.roll_trip(cluster=cluster, dest=var)

    if isinstance(value_to_console, list):
        # convert to JSON
        value_to_console = json.dumps(value_to_console)

    return value_to_console