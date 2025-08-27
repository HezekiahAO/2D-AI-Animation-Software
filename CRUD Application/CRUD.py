from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'   #SHOWS WHEWRE THE DATABASE IS LOCATED  THEY ARE ALL STORED IN THE USER DATABASE

db = SQLAlchemy(app)  # Initialize SQLAlchemy database with the Flask app

class user(db.Model):
    id = db.Column(db.Integer, unique= True, primary_key=True)
    Title_Task = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.Title_Task}>'  # __repr__ is a special method in Python that controls how an object is represented when you print it or inspect it in the console (e.g., typing the object name in a Python shell).

@app.route('/')
def root():
   return render_template('index.html')

if __name__ == '__main__':
    app.run(port = 5000, host = '0.0.0.0', debug=True)

