from flask import Flask                                                                                                      # IMPORT STAGE
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLAlchemy_DATABASE_URL'] = 'sqlite:///database.db'  # Set up your database
db = SQLAlchemy(app)
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort                                                # SET UP STAGE
api = Api(app)   # Thats our Api getting setup


class UserModel(db.Model):   #Creates a database model for users
    id = db.column(db.integer, primary_key=True)
    name = db.column(db.string(100), Unique=True, nullable=False)
    email = db.column(db.string(100), Unique=True, nullable = False)                                                           # SET UP CONTENTS AND CONDITIONS
                                                                                                                                
def __repr__(self):    # A representational File
    return f'User(name ={self.name}, email = {self.name})'   # A uniue represntation of a user


user_args = reqparse.RequestParser()
user_args.add_argument('name', type = str, required = True, help = 'Name cannot be left Blank chief')
user_args.add_argument('email', type = str, required = True, help = 'Email cannot be left Blank chief')
                    
@app.route("/")   # / gives the home page. TThat right after them come


def home():
    return "Hello Hezekiah, How was your day?"

if __name__ == "__main__":
    app.run(debug=True)