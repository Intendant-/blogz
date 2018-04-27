from flask import Flask, request, redirect, render_template, session, flash
from datetime import datetime
import cgi
from app import app, db
from model import User, Blog
from validation import required_field, password_validation, email_validation, db_validation, username_available

def blog_entries():
    return Blog.query.all()

def authors():
    return User.query.join(Blog, Blog.user_id == User.id).all()

allowed_routes = ['login', 'signup', 'index', 'blog']

@app.before_request
def require_login():
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')

@app.route('/')
def index():
    author = authors()
    return render_template('index.html', authors = author)

## ******************************************************* user login routes ********************************************************
## if user is logged in, do not show login link

@app.route('/login', methods=['GET', 'POST'])
def login():
    ## Query database for user/password
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_error = required_field(password)
        db_error = db_validation(username, password)
        if password_error or db_error:
            return render_template('login.html', password_error=password_error, db_error=db_error)

        else:
            session['user'] = username
            flash('Logged In')
            return redirect('/newpost')
    else:
        return render_template('login.html')
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    ## Create user in database
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        username_error = username_available(username)
        password_error = password_validation(password, verify)
        if username_error or password_error:
            return render_template('signup.html', username=username, username_error=username_error, password_error=password_error)
        ## TODO add availability error to template/render
        else:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            session['user'] = username
            flash('You have successfully signed up')
            return redirect('/newpost')
    else:
        return render_template('signup.html')    

@app.route('/logout')
def logout():
    del session['user']
    return redirect('/blog')

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():

    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['blog_text']
        user = User.query.filter_by(username=session['user']).first()
        blg_title = ''
        blg_text = ''
        if not title or not body:
            error = '**Please fill in both fields'
            blg_title = title
            blg_text = body
            return render_template('newpost.html', blog_title = blg_title, blog_text = blg_text, error= error)
        
        else:
            entry = Blog(title, body, user.id)
            db.session.add(entry)
            db.session.commit()
            return redirect('/blog?id={0}'.format(entry.id)) 
    else:  
        return render_template('newpost.html')


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    id = request.args.get('id')
    user_id = request.args.get('user_id')
    if id:
        post = Blog.query.filter_by(id=id).first()
        author = User.query.filter_by(id=post.user_id).first()
        return render_template('post.html', post = post, author=author)
    elif user_id:
        author = User.query.filter_by(id=user_id).first()
        posts = Blog.query.filter_by(user_id=user_id).all()
        return render_template('author.html', author=author, posts=posts)
    else:
        author = authors()
        return render_template('blog.html', blog_entries = blog_entries(), author='author') 


if __name__ == "__main__":
    app.run()