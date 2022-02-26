import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort
from FDataBase import FDataBase

# конфигурация

DATABASE = "/tmp/flsite.db"
DEBUG = True
SECRET_KEY = "sffasfageegdaxsfaghtr"

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, "flsite.db")))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    # Записи из базы данных представлены в виде словаря, а не кортежа
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Создадим БД без запуска сервера"""
    db = connect_db()
    with app.open_resource("sq_db.sql", mode="r") as f:
        # executescript - функция читает скрипты
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Соединение с базой данных, если оно еще не установлено"""
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template("index.html", menu=dbase.getMenu(), posts=dbase.getPostsAnonce() )


@app.teardown_appcontext # завершение обработки запроса
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if (len(request.form["name"]) > 4) and (len(request.form["post"]) > 10):
            res = dbase.addPost(request.form["name"], request.form["post"])
            if not res:
                flash("Ошибка добавления статьи", category="error")
            else:
                flash("Статья добавлена успешно", category="success")
        else:
            flash("Ошибка добавления статьи", category="success")
    return render_template("add_post.html", menu=dbase.getMenu(), title="добавление статьи")

@app.route("/post/<int:id_post>")
def showPost(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)

    return render_template("post.html", menu=dbase.getMenu(), title=title, post=post)


if __name__ == "__main__":
    app.run(debug=True)