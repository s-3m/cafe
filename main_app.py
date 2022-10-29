from pprint import pprint

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user

from db import get_db_connect
from models.model import Staff, Category, Dish, Order
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
            if post == 'официант':
                session['user_name'] = person.name
                return redirect(url_for("order_space"))
        flash("Неверный логин", "error")

    return render_template('index.html')


@app.route("/order_space/<cat_id>", methods=['POST', 'GET'])
@app.route("/order_space", methods=['POST', 'GET'])
@login_required
def order_space(cat_id=None):
    if request.method == "POST":
        table_num = request.form['table_number']
        if not session.get('order'):
            flash('Пустой заказ', 'err_flash')
        elif not table_num:
            flash('Не введен номер стола', 'err_flash')
        else:
            return redirect(url_for('confirm_order', tbl_num=table_num))

    if cat_id:
        dishes = sess.query(Dish).filter_by(category_id=int(cat_id))
    else:
        dishes = sess.query(Dish).all()
    pprint(session)
    category = sess.query(Category).all()
    return render_template('menu_for_waiters.html', category=category, dishes=dishes)


@app.route("/order_space/orders/<dish_id>")
def add_to_order(dish_id):
    print(request.referrer)
    try:
        check_category = int(request.referrer[-1])
    except ValueError:
        check_category = None
    if not session.get('order'):
        session['order'] = []
    session.modified = True
    session['order'].append(dish_id)
    print(session['order'])
    return redirect(url_for('order_space', cat_id=check_category))


@app.route("/confirm_order/<tbl_num>")
def confirm_order(tbl_num):
    for i in session.get('order'):
        new_order = Order(item_id=i, table_No=tbl_num)
        sess.add(new_order)
    sess.commit()
    del session['order']
    flash('Отправлено', 'success_flash')
    return redirect(url_for('order_space'))


@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
