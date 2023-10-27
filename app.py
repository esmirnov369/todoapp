from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description_what = db.Column(db.String(100))
    description_why = db.Column(db.String(100))
    completed = db.Column(db.Boolean)
    archived = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, nullable=False)
    date_completed = db.Column(db.DateTime)


@app.route("/")
def home():
    # todo_list_active = Todo.query.filter_by(archived="no")
    todo_list_active = Todo.query.filter_by(archived="no", completed=False)
    todo_list_completed = Todo.query.filter_by(archived="no", completed=True)
    return render_template(
        "base.html",
        todo_list_active=todo_list_active,
        todo_list_completed=todo_list_completed,
    )


@app.route("/add", methods=["POST"])
def add():
    description_what = request.form.get("description_what")
    description_why = request.form.get("description_why")
    new_todo = Todo(
        description_what=description_what,
        description_why=description_why,
        completed=False,
        archived="no",
        date_created=datetime.datetime.now(),
    )
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/complete/<int:todo_id>")
def complete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo.completed == False:
        todo.completed = True
        todo.date_completed = datetime.datetime.now()
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/uncomplete/<int:todo_id>")
def uncomplete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo.completed == True:
        todo.completed = False
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/archive/<int:todo_id>")
def archive(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo.archived == "no":
        todo.archived = "yes"
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/unarchive/<int:todo_id>")
def unarchive(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo.archived == "yes":
        todo.archived = "no"
    db.session.commit()
    return redirect(url_for("old"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("old"))


@app.route("/old")
def old():
    todo_list = Todo.query.filter_by(archived="yes")
    return render_template("archive.html", todo_list=todo_list)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
