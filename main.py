from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import os
import itertools 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo = True)
Session = sessionmaker(bind=engine)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)

def getNotes():
    db.drop_all()
    db.create_all()
    listOfNotes = os.listdir('./notes')
    for file in listOfNotes:
        with open('notes/' + file, "r") as f:
            title = file.split('.txt')[0]
            content = f.read()
            note = Note(title=title, content=content)
            print(note.title, note.content)
            db.session.add(note)
            db.session.commit() 

@app.route("/" , methods=['GET', 'POST'])
def index():
    getNotes()
    notes = Note.query.order_by(Note.id).all()
    return render_template('index.html', notes = notes)

@app.route("/note/<id>" , methods=['GET', 'POST'])
def note(id):
    getNotes()
    note = Note.query.filter_by(id=id).first()
    return render_template('note.html', note = note)

if __name__ == '__main__':
    app.run(debug=True)