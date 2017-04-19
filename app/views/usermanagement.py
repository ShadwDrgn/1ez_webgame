from app import app, mail
from flask import request, jsonify, render_template, Markup, url_for, redirect
from flask_mail import Message
from flask_login import login_user, logout_user
from .forms import LoginForm, RegisterForm
from app.game.player import User
from urllib.parse import urlparse


@app.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        print('got here')
        col = app.config['USERS_COLLECTION']
        user = col.find_one({"_id": form.username.data})
        if user and User.validate_login(user['passhash'], form.password.data):
            user_obj = User(user['_id'])
            if not user_obj.confirmed:
                template = render_template('alert.html',
                                           sev='warning',
                                           title='Warning!',
                                           message='Account not Activated.')
                return jsonify({'alert': template})
            login_user(user_obj)
            template = render_template('loggedin.html')
            return jsonify({'reset_socket': True, '#navright': template})
        template = render_template('alert.html',
                                   sev='danger',
                                   title='ERROR!',
                                   message='Bad username and/or password')
        return jsonify({"alert": template})


@app.route('/logout')
def logout():
    logout_user()
    markup = Markup('<li><a class="clickable" id="login" \
                    href="#login">Login</a></li>')
    return jsonify({'reset_socket': True, '#navright': markup})


@app.route('/signin')
def signin():
    form = LoginForm(request.form)
    template = render_template('login.html', form=form)
    return jsonify({'modal': '#bodyModal', '#bodyModal': template})


@app.route('/register', methods=['POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.add(form.username.data, form.email.data, form.password.data)
        token = User.generate_token(form.username.data)
        prefix = urlparse(request.url).scheme + \
            '://' + urlparse(request.url).netloc
        url = prefix + url_for('confirm', token=token)
        mail.send(Message('1.E.Z. EMail Confirmation',
                          recipients=[form.email.data],
                          html=url,
                          sender="noreply@1ez.us"))
        template = render_template('alert.html',
                                   sev='success',
                                   title='Registration!',
                                   message='Activation Email Sent.')
        return jsonify({'alert': template})


@app.route('/signup')
def signup():
    form = RegisterForm(request.form)
    template = render_template('register.html', form=form)
    return jsonify({'#bodyModal': template})


@app.route('/confirm/<token>')
def confirm(token):
    username = User.confirm_token(token)
    if not username:
        return 'invalid token'
    else:
        print(username)
        user = User.get(username)
        login_user(user)
        user.set_confirmed(True)
        return redirect(url_for("index"), code=302)
