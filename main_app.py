from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user

from db import get_db_connect
from models.model import Staff
from userlogin import UserLogin

app = Flask(__name__)

app.secret_key = b'_roman_1985_gmc'
login_manager = LoginManager(app)
sess = get_db_connect()


@login_manager.user_loader
def load_user(user_id):
    user = sess.query(Staff).filter_by(id=user_id).one()
    return UserLogin().create(user)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form['username']
        try:
            person = sess.query(Staff).filter_by(login=username).one()
        except:
            person = None
        if person:
            post = person.post.name
            log_user = UserLogin().create(person)
            login_user(log_user)
            if post == 'Официант':
                return redirect(url_for("order_space"))
        flash("Неверный логин", "error")
    return render_template('index.html')


@app.route("/order_space")
@login_required
def order_space():
    return render_template('menu_for_waiters.html')


@app.route("/logout")
def logout():
    logout_user()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
