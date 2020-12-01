from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db


@app.route('/')
@app.route('/home')
def homepage():
    title = {'title': 'Whats Happening In & Out of IC?'}
    body = {'body': 'Page is Under Construction. Apologizes in Advance!'}
    return render_template('base.html', title='Home', user=title, body=body)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('login')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
