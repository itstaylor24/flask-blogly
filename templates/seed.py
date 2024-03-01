from models import User, db
from app import app

db.drop_all()
db.create_all

taylor = User(first_name='Taylor', last_name='Harris')
angela = User(first_name='Angela', last_name='Osborne')

db.session.add(taylor)
db.session.add(angela)
db.session.commit()