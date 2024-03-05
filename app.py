"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User,Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "heyheyheyyou"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
 db.create_all()

@app.route('/')
def root_page():
    """Show recent list of posts, most-recent first."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("homepage.html", posts=posts)



@app.route('/users')
def list_users2():
    """Shows list of all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('userlist.html', users=users)


@app.route('/users/new', methods=["GET"])
def show_new_user_form():
    return render_template('createuser.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Creates a User"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
        
    db.session.add(new_user)
    db.session.commit()

    return redirect (url_for('list_users2'))
    

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """shows details on individual user"""
    user = User.query.get_or_404(user_id)
    return render_template('userdetails.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["GET"])
def show_edit_form(user_id):
    """shows edit form"""
    user = User.query.get_or_404(user_id)
    return render_template('useredit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def submit_edit_form(user_id):
    """updates a user"""
    user = User.query.get_or_404(user_id)
    user.first_name  = request.form['first_name'],
    user.last_name = request.form['last_name'],
    user.image_url = request.form['image_url'] or None 
            

    db.session.add(user)
    db.session.commit()
 
    return redirect("/users")

@app.route('/users/<int:user_id>/posts/new', methods = ['GET'])
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('post_form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def submit_post_form(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title =request.form['title'],
        content = request.form['content'], user=user)
    db.session.add(new_post)
    db.session.commit()
    return redirect (f"/users/{user_id}")

@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('post_edit_form.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    

    return redirect(f"/users/{post.user_id}")
    

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

     

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """deletes a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect ('/users')  


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")








            
     
 




    



