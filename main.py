import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import TodoForm

# initialize the Flask application
app = Flask(__name__)
# set a secret key for use for the flask form
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
# initialize the app to use bootstrap
Bootstrap(app)

# connect to db
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI", "sqlite:///Todo List.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TodoList(db.Model):
    """
    This class represents the TodoList table in the database
    """

    __tablename__ = "todo_list"
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(250), nullable=False)


# create the database if it does not exist
db.create_all()


# a route to the home page
@app.route("/")
def home():
    """
    This method is called when the home route is loaded on the web browser. It renders the home page
    :return: (str) the web page is rendered
    """

    todos = TodoList.query.all()

    return render_template("index.html", todos=todos)


# a route to the add todolist web page
@app.route("/add", methods=["GET", "POST"])
def add_todo():
    form = TodoForm()

    if form.validate_on_submit():
        new_todo = TodoList(todo=form.todo.data)
        db.session.add(new_todo)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add_todo.html", form=form)


# the route to delete API
@app.route("/delete/<int:todo_id>")
def delete_todo(todo_id):
    """
    This method is called when the user wants to delete a todolist
    :param todo_id: (int) the particular todolist to be deleted
    :return: None
    """

    # gets the todolist to be deleted from the database
    # delete the particular todolist form the database
    todo_to_delete = TodoList.query.get(todo_id)
    db.session.delete(todo_to_delete)
    db.session.commit()

    # redirect thr user back to the home page
    return redirect(url_for("home"))


# if this is the main class, run the app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
