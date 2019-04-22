from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, name, body):
        self.name = name
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blogpost_name = request.form['blogpost']
        blogpost_body = request.form['body']
        new_blogpost = Blog(blogpost_name,blogpost_body)
        db.session.add(new_blogpost)
        db.session.commit()

    blogposts = Blog.query.all()
    completed_blogposts = Blog.query.all()
    return render_template('home.html',title="< My blog >", 
        blogposts=blogposts, completed_blogposts=completed_blogposts)

@app.route('/new_post', methods=['GET','POST'])
def new_post():    
    message = ""
    if request.method == 'POST':
        blogpost_name = request.form['blogpost']
        blogpost_body = request.form['body']
        if len(blogpost_name) <3 or len(blogpost_body) <3:
            message = "Your blog title or content is too short."
            
        else:
            message = "Success!"
            new_blogpost = Blog(blogpost_name,blogpost_body)
            db.session.add(new_blogpost)
            db.session.commit()
            return render_template('blogpost.html',title="< My blog >", 
            blogpost_name=blogpost_name, blogpost_body=blogpost_body)
    
    blogposts = Blog.query.all()
    completed_blogposts = Blog.query.all()
    return render_template('new_post.html',title="< My blog >", 
        message=message, completed_blogposts=completed_blogposts)
    

@app.route('/blogpost', methods=['GET'])
def blogpost():
    blogpost_id = request.args.get("blogpost-id")
    blogpost = Blog.query.get(blogpost_id)
    blogpost_name = blogpost.name
    blogpost_body = blogpost.body
    return render_template('blogpost.html', 
        blogpost_name=blogpost_name, blogpost_body=blogpost_body)

@app.route('/delete-blogpost', methods=['POST'])
def delete_blogpost():

    blogpost_id = int(request.form['blogpost-id'])
    blogpost = Blog.query.get(blogpost_id)
    blogpost.completed = True
    db.session.add(blogpost)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()