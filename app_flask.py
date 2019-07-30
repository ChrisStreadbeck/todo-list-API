# This is using just flask, not marshmallow.

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)

db = SQLAlchemy(app)

# to this point it's boilerplate.  Code Snippet?
# pipenv install, run things in the shell.
# make sure you install flask, and the flask alchemy / cors etc. to your pipenv before running the prog.
# in pipenv, enter python, from app import db, db.create_all()

class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False) # 100 = character limit, nullable means has to have some input (can't be empty)
    done = db.Column(db.Boolean)


    def __init__(self, title, done):
        self.title = title
        self.done = done

@app.route("/todos", methods=["GET"])
def get_todos():
    all_todos = db.session.query(Todo.id, Todo.title, Todo.done).all()
    return jsonify(all_todos)

@app.route("/add-todo", methods=["POST"])
def add_todo():
    if request.content_type == "application/json":
       post_data = request.get_json()

       title = post_data.get("title")
       done = post_data.get("done")

       record = Todo(title, done)
       db.session.add(record)
       db.session.commit()
       return jsonify([record.id, record.title, record.done])
    return jsonify("Check content_type and try again")

@app.route("/todo/<id>", methods=["PUT"])
def update_todo(id):
    if request.content_type == "application/json":
       put_data = request.get_json()

       title = put_data.get("title")
       done = put_data.get("done")

       record = db.session.query(Todo).get(id)
       record.title = title
       record.done = done 
       
       db.session.commit()
       return jsonify("Update Successful")
    return jsonify("Check content_type and try again")

@app.route("/todo/<id>", methods=["DELETE"])
def delete_todo(id):
    record = db.session.query(Todo).get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify("Record DELETED!!")    

# if __name__ =="__main__":
 #   app.debug = True
 #   app.run()