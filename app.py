from os import name
import flask
from flask import request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = flask.Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(50), nullable=False, default="Anonymous")
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "Blog Post " + str(self.id)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = Card.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/login', methods=['GET', 'POST'])
def login(id):

    if request.method == "POST":
        post = Card.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('login.html')


@app.route('/posts/edit/<int:id>', methods=["GET", "POST"])
def edit(id):

    if request.method == "POST":
        post = Card.query.get_or_404(id)
        post.name = request.form['name']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template("edit.html", post=Card.query.get_or_404(id))


@app.route('/posts', methods=["GET", "POST"])
def posts():

    if request.method == "POST":
        postName = request.form['name']
        postContent = request.form['content']
        newCard = Card(name=postName, content=postContent)
        db.session.add(newCard)
        db.session.commit()
        return redirect('/posts')

    else:
        allPosts = Card.query.order_by(Card.id.desc()).all()
        return(
            flask.render_template('posts.html', posts=allPosts)
        )


@app.route("/")
def index():
    return(
        flask.render_template('index.html')
    )


if __name__ == '__main__':
    app.run(debug=True)
