from flask import Flask, render_template, request, redirect
import cgi
import os
import string

# set up flask
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/welcome')
def welcome():
    name = request.args.get('username')
    return render_template('welcome.html', name = name, title = 'Welcome')

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']
        error_u = ''
        error_p = ''
        error_v = ''
        error_e = ''
        if not username:
            error_u = 'You left this blank. Please type in your username.'
            username = ''
        elif len(username) < 3 or len(username) > 20:
            error_u = 'Invalid length: either less than 3 or more than 20.'
            username = ''
        elif check_space(username):
            error_u = 'Space character(s) found. Omit space(s).'
            username = ''
        if not password:
            error_p = 'You left this blank. Please type in a valid password.'
            password = ''
        elif len(password) < 3 or len(password) > 20:
            error_p = 'Invalid length: either less than 3 or more than 20.'
            password = ''
        elif check_space(password):
            error_p = 'Space character(s) found. Omit space(s).'
            password = ''
        elif not is_strong(password):
            error_p = 'Password is not strong enough. Please type in a valid password'
            password = ''
        if not verify:
            error_v = 'You left this blank. Please verify password.'
            password = ''
            verify = ''
        elif password != verify:
            error_v = 'Passwords don\'t match.'
            password = ''
            verify = ''
        if email:
            at_count = 0
            dot_count = 0
            for i in email:
                if i == '@':
                    at_count += 1
                elif i == '.':
                    dot_count += 1
            if len(email) < 3 or len(email) > 20:
                error_e = 'Invalid email length: either less than 3 or more than 20.'
                email = ''
                password = ''
                verify = ''
            elif check_space(email):
                error_e = 'Space character(s) found. Omit space(s).'
                email = ''
                password = ''
                verify = ''
            elif at_count > 1 or dot_count < 1:
                error_e = 'Please type in a valid email address.'
                email = ''
                password = ''
                verify = ''
        if not error_u and not error_p and not error_v and not error_e:
            return redirect('/welcome?username={0}'.format(username))
        else:
            return render_template('signup.html',
                title = 'User Signup',
                username = username,
                password = password,
                verify = verify,
                email = email,
                error_u = error_u,
                error_p = error_p,
                error_v = error_v,
                error_e = error_e)
    return render_template('signup.html', title = 'User Signup')
def check_space(token):
    for i in token:
        if i == ' ':
            return True
    return False

def is_strong(password):
    lower = False
    upper = False
    number = False
    special = False
    for i in password:
        if i.islower():
            lower = True
        elif i.isupper():
            upper = True
        elif i.isdigit():
            number = True
        elif i in string.punctuation:
            special = True
    return lower and upper and number and special

app.run()