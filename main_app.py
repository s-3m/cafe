from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user

from db import get_db_connect
from models.model import Staff, Category, Dish
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
    category = sess.query(Category).all()
    dishes = sess.query(Dish).all()
    return render_template('menu_for_waiters.html', category=category, dishes=dishes)


@app.route("/order_space/<cat_id>")
def menu_on_category(cat_id):
    sort_dish = sess.query(Dish).filter_by(category_id=int(cat_id))
    category = sess.query(Category).all()
    return render_template('menu_for_waiters.html', category=category, dishes=sort_dish)


order_list = []


@app.route("/order_space/orders/<dish_id>")
def add_to_order(dish_id):
    order_item = sess.query(Dish).filter_by(id=dish_id).one()
    order_list.append(order_item)
    print(order_list)
    return redirect(url_for(f'menu_on_category', cat_id=order_item.category_id))


@app.route("/logout")
def logout():
    logout_user()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
