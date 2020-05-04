from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)


all_posts = [
    {
        'title': 'post1',
        'content': 'hi there buddy how u doun'
    },
    {
        'title': 'post2',
        'content': 'hi man how buddy how u doun'
    }
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = BlogPost(
            title=post_title, content=post_content, author='subh')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.all()
        return render_template('posts.html', posts=all_posts)


@app.route('/home/<string:name>')
def hello(name):
    return 'hello world '+name


if __name__ == '__main__':
    app.run(debug=True)
