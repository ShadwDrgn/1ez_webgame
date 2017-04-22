import json
from flask import jsonify, request, after_this_request, Markup, render_template
from app import app
import flask_security
from app.views.forms.extendedlogin import ExtendedLoginForm


@app.route('/applogin', methods=['GET', 'POST'])
def applogin():
    if request.method == "GET":
        template = flask_security.views.login()
        return jsonify({'modal': '#bodyModal', '#bodyModal': template})
    if request.method == "POST":
        form = flask_security.views._security.login_form()
        if form.validate_on_submit():
            flask_security.utils.login_user(form.user,
                                            remember=form.remember.data)
            after_this_request(flask_security.views._commit)
            template = render_template('account/loggedin.html')
            return jsonify({'reset_socket': True, '#navright': template})
        else:
            template = render_template('alert.html',
                                       sev='danger',
                                       title='ERROR!',
                                       message='Bad username and/or password')
            return jsonify({"alert": template})


@app.route('/applogout')
def applogout():
    flask_security.utils.logout_user()
    markup = Markup('<li><a class="clickable" id="login" \
                    href="#login">Login</a></li>')
    return jsonify({'reset_socket': True, '#navright': markup})


@app.route('/appregister', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        form = ExtendedLoginForm()
        template = render_template('account/register.html',
                                   register_user_form=form)
        return jsonify({'modal': '#bodyModal', '#bodyModal': template})
    if request.method == "POST":
        form = ExtendedLoginForm(request.form)
        if form.validate_on_submit():
            user = flask_security.registerable.register_user(**form.to_dict())
            form.user = user
            template = render_template('alert.html',
                                       sev='success',
                                       title='Registration!',
                                       message='Activation Email Sent.')
            return jsonify({'alert': template})
        print(json.dumps(form.errors))
        return None