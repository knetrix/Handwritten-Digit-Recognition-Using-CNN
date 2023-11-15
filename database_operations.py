import os
import sqlite3
import sys
import threading
import webbrowser

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import InternalServerError

app = Flask("database")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class image_prediction_table(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    image_path = db.Column(db.String, unique=True, nullable=True)
    prediction = db.Column(db.String, unique=False, nullable=True)
    correctness = db.Column(db.String, unique=False, nullable=True)
    is_prediction_correct = db.Column(
        db.String, unique=False, nullable=True, default="unchecked"
    )


class success_rate_table(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    success_rate = db.Column(db.String, unique=False, nullable=False)


db.create_all()


sys.tracebacklimit = 0  # traceback görüntülenmemesi için
database_connection = sqlite3.connect("database.db", check_same_thread=False)
database_cursor = database_connection.cursor()

database_cursor.execute(
    """DELETE FROM success_rate_table""",
)
database_connection.commit()

database_cursor.execute(
    """INSERT INTO success_rate_table (success_rate) VALUES ('No Data.')""",
)
database_connection.commit()


def update_data():
    database_cursor.execute("""SELECT * FROM image_prediction_table""")
    return (
        database_cursor.fetchall()
    )  # tablodaki verileri fetchall fonksiyonu ile veriler değişkenine alıyorum


def add_database_record(data):
    database_cursor.execute(
        """INSERT INTO image_prediction_table (image_path,prediction,correctness) VALUES
                (?, ?, ?)""",
        data,
    )
    database_connection.commit()


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Login Information is Incorrect. Try again!"
        else:
            return redirect(url_for("View_Database"))
    return render_template("login_page.html", error=error)


@app.route("/")
def View_Database():
    view_database = image_prediction_table.query.paginate()
    success_rate_filter = success_rate_table.query.filter_by(id=1).first()
    return render_template(
        "database_page.html",
        view_database=view_database,
        success_rate=success_rate_filter.success_rate,
    )


id_list = []


@app.route("/", methods=["GET", "POST"])
def update_database():
    global id_list
    if request.method == "POST":
        database_all_data = update_data()
        checkbox_selected_list = request.form.getlist(
            "prediction"
        )  # Checkbox Input Name

        for i in range(len(database_all_data)):
            id_list.append(database_all_data[i][0])

        if len(database_all_data) == 0:
            success_rate = "No Data."
            database_cursor.execute(
                """UPDATE success_rate_table SET success_rate = (?) WHERE id = 1""",
                (success_rate,),
            )
            database_connection.commit()
        else:
            success_rate_int = (
                len(checkbox_selected_list) / len(database_all_data)
            ) * 100
            success_rate = "%" + str(round(success_rate_int, 2))

            database_cursor.execute(
                """UPDATE success_rate_table SET success_rate = (?) WHERE id = 1""",
                (success_rate,),
            )
            database_connection.commit()

        for i in checkbox_selected_list:
            data = i
            database_cursor.execute(
                """UPDATE image_prediction_table SET is_prediction_correct = 'checked' WHERE id = (?)""",
                (data,),
            )
            database_connection.commit()

        for y in id_list:
            y = str(y)
            if y not in checkbox_selected_list:
                data = y
                database_cursor.execute(
                    """UPDATE image_prediction_table SET is_prediction_correct = 'unchecked' WHERE id = (?)""",
                    (data,),
                )
                database_connection.commit()
        id_list = []

    return redirect(url_for("View_Database"))


app.secret_key = "super secret key"


@app.route("/delete/<int:id>", methods=["POST", "GET"])
def Database_DeleteRow(id):
    try:
        data = image_prediction_table.query.get(id)
        id_row = image_prediction_table.query.filter_by(id=id).first()
        image_name = id_row.image_path
        path = os.path.join(os.getcwd() + "\\static\\", image_name)
        os.remove(path)

        db.session.delete(data)
        db.session.commit()
        return redirect(url_for("View_Database"))
    except Exception as e:
        print("Error: " + str(e))


@app.errorhandler(InternalServerError)
def handle_500(e):
    original = getattr(e, "Hata", None)
    return render_template("error_page.html", e=original)


i = 0


def run():
    global i
    i = i + 1
    if i == 1:
        webbrowser.open_new("http://127.0.0.1:5000/login")
        app.run(debug=False)


def run_threading():
    t1 = threading.Thread(target=run)
    t1.start()
