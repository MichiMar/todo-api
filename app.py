from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Herooku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    done = db.Column(db.Boolean)

    def __init__(self, title, done):
        self.title = title
        self.done = done

class TodoSchema(ma.Schema):
    class Meta:
        fields = ("id", "title","done")
        
todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

# alwayw two arguments
@app.route("/todos", methods=["GET"])
def get_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result)

@app.route("/todo", methods=["POST"])
def add_todo():
    title = request.json["title"]
    done = request.json["done"]

    new_todo = Todo(title, done)
    db.session.add(new_todo)
    db.session.commit()
    
    created_todo = Todo.query.get(new_todo.id)
    return todo_schema.jsonify(created_todo)

@app.route("/todo/<id>", methods=["PUT"])
def update_todo(id):
    todo = Todo.query.get(id)

    todo.title = request.json["title"]
    todo.done = request.json["done"]

    db.session.commit()
    return todo_schema.jsonify(todo)

@app.route("/todo/<id>", methods=["DELETE"])
def delete_todo(id):
    todo = Todo.query.get(id)

    db.session.delete(todo)
    db.session.commit()

    return "RECORD DELETED"

if __name__ == "__main__":
    app.debug = True
    app.run()

    response