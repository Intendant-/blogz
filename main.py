from flask import Flask, request, redirect, render_template, session, flash
from datetime import datetime
import cgi
from app import app, db
from model import User, Blog

def blog_entries():
    return Blog.query.all()

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['blog_text']
        blg_title = ''
        blg_text = ''
        if not title or not body:
            error = '**Please fill in both fields'
            blg_title = title
            blg_text = body
            return render_template('newpost.html', blog_title = blg_title, blog_text = blg_text, error= error)
        # TODO validate form title and body
        else:
            entry = Blog(title, body)
            db.session.add(entry)
            db.session.commit()
            return redirect('/blog?id={0}'.format(entry.id)) 
    else:  
        return render_template('newpost.html')

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    id = request.args.get('id')
    if id:
        post = Blog.query.filter_by(id=id).first()
        return render_template('post.html', post = post)
    else:
        return render_template('blog.html', blog_entries = blog_entries()) 

@app.route("/blog?id=")
def post():
    id = request.args.get('id')
    return render_template('post.html', entry=entry)

if __name__ == "__main__":
    app.run()      