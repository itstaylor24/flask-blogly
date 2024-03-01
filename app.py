"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
def list_users():
    """Shows list of all users"""
    users = User.query.all()
    return redirect('/users')

@app.route('/users')
def list_users2():
    """Shows list of all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('userlist.html', users=users)


@app.route('/users/new', methods=["GET","POST"])
def create_user():
    """Creates a User"""
    if request.method =="POST":

        new_user = User(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            image_url=request.form['image_url'] or None)
        
        db.session.add(new_user)
        db.session.commit()

        return redirect (url_for('list_users2'))
    return render_template('createuser.html')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """shows details on individual user"""
    user = User.query.get_or_404(user_id)
    return render_template('userdetails.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    """shows edit form"""
    user = User.query.get_or_404(user_id)
    return render_template ('useredit.html', user=user)

@app.route('/users/<int:user_id>/edit',  methods = ["GET", "POST"])
def update_edit_form(user_id):
    """updates a user"""
    if request.method =="POST":
        user = User.query.get_or_404(user_id)
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")
     

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """deletes a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect ('/users')  