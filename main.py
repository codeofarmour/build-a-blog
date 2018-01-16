from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:cheese@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'bJxc3x9ex8exb3ax03MSxecx8axcdxc3x14}'

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(510))    
    def __init__(self, title, body):
        self.title=title
        self.body=body    

@app.route('/')
def index():
    return redirect('/blog')   

@app.route('/blog', methods = ['POST', 'GET'])
def blog():    

    id = request.args.get('id')
    if id:
        blog = Blog.query.filter_by(id=id).first()
        return render_template('individual.html', blog=blog)
    else:
        blogs = Blog.query.order_by(Blog.id.desc()).all()
        return render_template('blog.html', blogs = blogs)
    
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'GET':
        return render_template('newpost.html', title='', body='', blog_error='')
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        blog_error=''        
    if title=='' or body=='':
        blog_error='Both a title and a body are required.'
        
    if blog_error=='':
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        new_id = new_blog.id
        return redirect('/blog?id='.format(new_id))          
    else:
        return render_template('newpost.html', blog_error=blog_error, title=title, body=body)

if __name__ == '__main__':
    app.run()