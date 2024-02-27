"""Blogly application."""

from flask import Flask, request, redirect, render_template
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

@app.route('/')
def list_users():
    """Shows list of all users"""
    users = User.query.all()
    return render_template('userlist.html', users=users)

@app.route('/users')
def list_users():
    """Shows list of all users"""
    users = User.query.all()
    return render_template('userlist.html', users=users)

@app.route('/users/new')
def show_create_form():
    """Shows form to create a user"""

    
    return render_template('createuser.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Creates a User"""
    
    first_name= request.form['first_name']
    last_name= request.form['last_name']
    image_url= request.form['image_url']
    return redirect ('/users')

@app.route('/users/<user-id>')
def show_user(user-id):
    """shows details on individual user"""
    user = User.query.get_or_404(user-id)
    return render_template ('userdetail.html', user=user)

@app.route('/users/<user-id>/edit')
def show_edit_form(user-id):
    """shows edit form"""
    user = User.query.get_or_404(user-id)
    return render_template ('useredit.html', user=user)

@app.route('/users/<user-id>/edit', methods['POST'])
def update_edit_form():
    """updates a user"""
    
    return redirect ('/users')   

@app.route('/users/[user-id]/delete', methods['POST'])
def delete_user():
    """updates a user"""
    
    return redirect ('/users')  