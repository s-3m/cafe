import time

# from gevent import monkey; monkey.patch_all()
# from gevent.pywsgi import WSGIServer
from pprint import pprint
from time import sleep

from flask import Flask, render_template, request, flash, redirect, url_for, session, Response
from flask_login import LoginManager, login_user, login_required, logout_user

from db import get_db_connect
from models.model import Staff, Category, Dish, Order, OrderItems, Status
from userlogin import UserLogin

app = Flask(__name__)

app.secret_key = b'_roman_1985_gmc'
login_manager = LoginManager(app)
sess = get_db_connect()

serv_msg = {

}


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
            post = person.post.name.lower()
            log_user = UserLogin().create(person)
            login_user(log_user)
            if post == 'официант':
                session['user_name'] = person.name
                return redirect(url_for("waiter_start"))
        flash("Неверный логин", "alert alert-danger")

    return render_template('index.html')


@app.route('/waiter_start')
def waiter_start():
    staff = sess.query(Staff).filter_by(id=int(session.get('_user_id'))).one()
    return render_template('waiter_start.html', staff=staff)


@app.route('/new_order')
def create_new_order():
    # new_order = Order(staff_id=int(session.get('_user_id')))
    # sess.add(new_order)
    # sess.commit()
    return redirect(url_for('order_space'))


@app.route("/order_space/<cat_id>", methods=['POST', 'GET'])
@app.route("/order_space", methods=['POST', 'GET'])
@login_required
def order_space(cat_id=None):
    if request.method == "POST":
        table_num = request.form['table_number']
        if not session.get('order'):
            flash('Пустой заказ', 'alert alert-danger')
        elif not table_num:
            flash('Не введен номер стола', 'alert alert-danger')
        else:
            return redirect(url_for('confirm_order', tbl_num=table_num))

    if cat_id:
        dishes = sess.query(Dish).filter_by(category_id=int(cat_id))
    else:
        dishes = sess.query(Dish).all()
    category = sess.query(Category).all()
    staff = sess.query(Staff).filter_by(id=int(session.get('_user_id'))).one()
    return render_template('menu_for_waiters.html', category=category, dishes=dishes, staff=staff)


@app.route("/order_space/orders/<dish_id>")
def add_to_order(dish_id):
    try:
        check_category = int(request.referrer[-1])
    except ValueError:
        check_category = None
    if not session.get('order'):
        session['order'] = []
    session.modified = True
    session['order'].append(dish_id)
    return redirect(url_for('order_space', cat_id=check_category))


@app.route("/confirm_order/<tbl_num>")
def confirm_order(tbl_num):
    new_order = Order(staff_id=int(session.get('_user_id')), table_No=tbl_num, status=7)
    try:
        sess.add(new_order)
        sess.commit()
    except:
        print('Ошибка добавления заказа в БД')
    for i in session.get('order'):
        new_item = OrderItems(item_id=i, order_num=new_order.number)
        try:
            sess.add(new_item)
        except:
            print(f'Ошибка добавления позиции "{i}" в заказ')
    sess.commit()
    del session['order']
    flash('Отправлено', 'alert alert-success')
    serv_msg['msg'] = 'sssssssssssssssssssssssssssssssssssssssss'
    return redirect(url_for('waiter_start'))


@app.route('/history')
def order_history():
    orders = sess.query(Order).filter_by(staff_id=int(session.get('_user_id'))).all()
    return render_template('order_history.html', orders=orders)


@app.route('/order/<order_id>')
def order_items(order_id):
    items = sess.query(OrderItems).filter_by(order_num=order_id).all()
    return render_template('order_items.html', items=items)


@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))


def data_stream():
    while True:
        yield f"data: {serv_msg.get('msg')}\n\n"
        time.sleep(10)
        serv_msg.clear()


@app.route('/listen')
def listen():
    return Response(data_stream(), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
