from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_ECHO'] = True
UPLOAD_FOLDER = 'notes'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo = True)
Session = sessionmaker(bind=engine)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    preview = db.Column(db.String(200), nullable=False)

def getFirstLine(file):
    file = file + '.txt'
    with open('notes/' + file, "r") as f:
        firstLine = f.readline()
        return firstLine

def getNotes():
    db.drop_all()
    db.create_all()
    listOfNotes = os.listdir('./notes')
    for file in listOfNotes:
        with open('notes/' + file, "r") as f:
            title = file.split('.txt')[0]
            content = f.read()
            preview = getFirstLine(title) + '...'
            note = Note(title=title, content=content, preview=preview)
            db.session.add(note)
            db.session.commit()

@app.route("/" , methods=['GET', 'POST'])
def index():
    getNotes()
    notes = Note.query.order_by(Note.id).all()
    return render_template('index.html', notes = notes)

@app.route("/option", methods=['GET', 'POST'])
def chooseUpload():
    return render_template('option.html')

@app.route("/note/<id>" , methods=['GET', 'POST'])
def note(id):
    getNotes()
    note = Note.query.filter_by(id=id).first() 
    return render_template('note.html', note = note)

@app.route("/upload" , methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')

@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        print("=======================================")
        print(f.filename)
        if f.filename.split('.')[1] in ALLOWED_EXTENSIONS:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return redirect('/')
        else:
            return "Wrong file format"
    else:
        return redirect('/upload')


@app.route("/write_note", methods=['GET', 'POST'])
def write_note():
    return render_template('write.html')

@app.route("/writer", methods=['GET', 'POST'])
def writer():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = open('notes/' + title + '.txt', 'w')
        file.write(content)
        file.close()
        return redirect('/')
    else:
        return render_template('write.html')

if __name__ == '__main__':
    app.run(debug=True)