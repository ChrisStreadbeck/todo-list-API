from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ffnlyjrjyzvlco:01fa92b9d1d9eb14aa8971159e13f265ec815afb26b52e25c1276481412c04fb@ec2-54-235-92-43.compute-1.amazonaws.com:5432/ddpvmgq9up4pgj")

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False) # 100 = character limit, nullable means has to have some input (can't be empty)
    done = db.Column(db.Boolean)


    def __init__(self, title, done):
        self.title = title
        self.done = done

class TodoSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "done")

todos_schema = TodoSchema(many=True)
todo_schema = TodoSchema()



@app.route("/todos", methods=["GET"])
def get_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)

    return jsonify(result.data)

@app.route("/add-todo", methods=["POST"])
def add_todo():
    title = request.json["title"]
    done = request.json["done"]
    record = Todo(title, done)
    db.session.add(record)
    db.session.commit()

    todo = Todo.query.get(record.id)
    return todo_schema.jsonify(todo)


@app.route("/todo/<id>", methods=["PUT"])
def update_todo(id):
    todo=Todo.query.get(id)

    title = request.json["title"]
    done = request.json["done"]

    todo.title = title
    todo.done = done 
    
    db.session.commit()
    return jsonify("Update Successful")


@app.route("/todo/<id>", methods=["DELETE"])
def delete_todo(id):
    record = Todo.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify("Record DELETED!!")    

if __name__ =="__main__":
    app.debug = True
    app.run()