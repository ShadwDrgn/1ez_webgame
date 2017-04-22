from flask import render_template, Markup, jsonify
from app import app


@app.route('/')
@app.route('/index')
def index():
    nav_items = ['Updates', 'Map', 'Items', 'Location']
    return render_template('index.html',
                           title='1.E.Z.',
                           nav_items=nav_items)


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
