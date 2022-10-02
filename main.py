from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import os
import itertools 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo = True)

Session = sessionmaker(bind=engine)


class Note:
    newid = itertools.count().__next__
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.id = Note.newid()

    def getTitle(self):
        return self.title
    def getContent(self):
        return self.content
    def getId(self):
        return self.id

# class Note(Base):
#     __tablename__ = 'note'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable = False)
#     content = db.Column(db.String(200), nullable = False)

allNotes = os.listdir('./notes')
notes = []
for i in allNotes:
    with open('notes/' + i, 'r') as f:
        note = Note(i, f.read())
        print(note.title)
        notes.append(note)

# db.session.add(Note(title = 'test', content = 'this is a test'))
# db.session.commit()
# db.session.add(Note(title = 'test2', content = 'this is a second test'))
# db.session.commit()

@app.route("/")
def index():
    return render_template('index.html', notes = notes)
    # return render_template('note.html', notes=notes)

@app.route('/note/<id>')
def note(id):
    for i in notes:
        if i.getId() == int(id):
            return render_template('note.html', note = i)

if __name__ == '__main__':
    app.run(debug=True)