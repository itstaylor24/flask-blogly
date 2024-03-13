"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
# What is special anout url_for?
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User,Post, Tag, PostTag


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "heyheyheyyou"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# Connects the flask app to SQL Alchemy
app_context = app.app_context()
app_context.push()
    # don't understand why above line is needed
    # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/contexts/
db.create_all()

@app.route('/')
def root_page():
    """Show recent list of posts, most-recent first."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    # shows all rows of posts and orders them by 
    # the created_at Column in descending order and only the first 5 
    return render_template("homepage.html", posts=posts)
    # renders the homepage template which we pass the posts variable into



@app.route('/users')
def list_users2():
    """Shows list of all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    # returns all users in a list and orders them by  last name and then first name
    return render_template('userlist.html', users=users)
    # we render the users template and pass in the users variable


@app.route('/users/new', methods=["GET"])
def show_new_user_form():
    return render_template('createuser.html')
    # retrieves the template that creates a user

@app.route('/users/new', methods=["POST"])
def create_user():
    """Creates a User"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
        # this creates a new instance of a User
        
    db.session.add(new_user)
    # What is session in this context?
    db.session.commit()

    return redirect (url_for('list_users2'))
    

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """shows details on individual user"""
    user = User.query.get_or_404(user_id)
    # we take the user_id from an individual user

    return render_template('userdetails.html', user=user)
    # This returns the details on that specific user


@app.route('/users/<int:user_id>/edit', methods=["GET"])
def show_edit_form(user_id):
    """shows edit form"""
    user = User.query.get_or_404(user_id)
    # retrieves the id of a specific user
    return render_template('useredit.html', user=user)
    # renders an edit page for that specific user

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def submit_edit_form(user_id):
    """updates a user"""
    user = User.query.get_or_404(user_id)
    user.first_name  = request.form['first_name'],
    user.last_name = request.form['last_name'],
    user.image_url = request.form['image_url'] or None 
    # retrieves the values which are already inside of the inputs
            

    db.session.add(user)
    db.session.commit()
 
    return redirect("/users")

@app.route('/users/<int:user_id>/posts/new', methods = ['GET'])
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.order_by(Tag.name).all()
    
    # allows a user to post by accessing their specific user id, the .get method is used only for primary keys
    return render_template('post_form.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def submit_post_form(user_id):
    user = User.query.get_or_404(user_id)
    # tag_ids = [int(num) for num in request.form.getlist("tags")]
    # tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    # don't understand

    new_post = Post(
        title =request.form['title'],
        content = request.form['content'], user=user)
    db.session.add(new_post)
    db.session.commit()
    return redirect (f"/users/{user_id}")
    # why do we use the f string in redirection but the greater than or less than symbols is the route url?

@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('post_edit_form.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    # retrieves a specific post id
    post.title = request.form['title']
    # 
    post.content = request.form['content']

    # tag_ids = [int(num) for num in request.form.getlist("tags")]
    # post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    

    return redirect(f"/users/{post.user_id}")
    # why not '/posts/<int:post_id>'?

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

@app.route('/tags')
def tags_list():
    """lists of all tags"""
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('tags_list.html', tags=tags)

@app.route('/tags/<tag_id>')
def tag_details_show(tag_id):
    """shows details on specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    
    return render_template('tag_details.html', tag=tag)

@app.route('/tags/new')
def show_tag_form():
    """shows form to add a new tag"""
    posts= Post.query.all()
    return render_template('new_tag_form.html',posts=posts)

@app.route('/tags/new', methods= ['POST'] )
def submit_tag_form():
    """handles submission of tag form"""
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)
    # definitely don't understand the above line of code, i just added it
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')



@app.route('/tags/<tag_id>/edit')
def edit_tag_form(tag_id):
    """shows form to edit a tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
   
    return render_template('edit_tag_form.html' , tag=tag, posts=posts)

@app.route('/tags/<tag_id>/edit', methods=['POST'])
def handle_edit_tag_form():
    """handles form to edit a tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")

@app.route('/tags/<tag_id>/delete', methods=['POST'] )
def delete_tag(tag_id):
    """deletes a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')













            
     
 




    



