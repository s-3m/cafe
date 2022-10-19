from flask import Flask, render_template, request, flash

from db import get_db_connect
from models.model import Staff
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form['username']
        sess = get_db_connect()
        person = sess.query(Staff).filter_by(login=username).one()
        post = person.post.name
        if post == 'Официант':
            return render_template('for_waiter.html', person=person.name)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
