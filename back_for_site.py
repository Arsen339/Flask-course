from flask import Flask, render_template, url_for, request, flash, session, redirect, url_for, abort

app = Flask(__name__)
app.config["SECRET_KEY"] = 'fwegfasdfgfhytjy875udu'
menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Певое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]
# одинаковый ответ на разные url


@app.route("/index")
@app.route("/")
def index():
    print(url_for("index"))  # вернет /
    return render_template("index.html", info_index="Index page here", menu=menu)


@app.route("/about")
def about():
    print(url_for("about"))
    # вернем url адрес
    return render_template("about.html", title="Описание", info_about="Description here")



@app.route("/contact", methods=["POST", "GET"]) # допишем методы получения информации
def contact():
    if request.method == 'POST':
        # считаем информацию из формы
        print(request.form)
        print(request.form['message'])

        if len(request.form['username']) > 2:
            # отправим мнгновенное сообщение с помощью функции flash
            flash("Сообщение отправлено", category="success")
        else:
            flash('Ошибка отправки', category="error")
    return render_template("contact.html", title="Обратная связь", menu=menu)


# создадим декоратор обработки ошибок сервера
@app.errorhandler(404)
def pageNotFound(error):
    return render_template("page404.html", title="Страница не найдена", menu=menu)


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        # если свойство userLogged существует в сессии, делаем переадресацию на профиль
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "Arsen" and request.form['psw'] == "123":
        # если вошел данный пользователь:
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="Авторизация", menu=menu)


@app.route("/profile/<username>")
def profile(username):
    # Авторизация пользователя
    if ('userLogged' not in session) or (session["userLogged"] != username):
        # если пользователь не зашел или имя не совпадает
        abort(401)
    return f"Пользователь: {username}"


with app.test_request_context():
    # выведем url
    print(url_for("index"))
    print(url_for("about"))
    print(url_for("profile", username="user"))
    print(url_for("contact"))
    print(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)


