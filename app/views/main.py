from flask import render_template, Markup, request, jsonify
from .forms import LoginForm
from app import app


@app.route('/')
@app.route('/index')
def index():
    nav_items = ['Updates', 'Map', 'Items', 'Location']
    form = LoginForm(request.form)
    return render_template('index.html',
                           title='1.E.Z.',
                           nav_items=nav_items,
                           form=form)


@app.route('/Updates')
def updates():
    desc = """
    Login/Register moved to modal<br />
    Email activation works<br />
    Registration works<br />
    """
    template = render_template('update.html',
                               summary='Modularize',
                               desc=Markup(desc))
    return jsonify({'#content': template})


@app.route('/Map')
def map():
    template = render_template('map.html')
    return jsonify({'#content': template})
