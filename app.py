from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from config import db_password

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:{}@localhost/users'.format(db_password)
db = SQLAlchemy(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'super secret key'



class userData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    dist = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    dose = db.Column(db.String(120), nullable=False)

    def __init__(self, email, dist, age, dose):
        self.email = email
        self.dist = dist
        self.age = age
        self.dose = dose

    def __repr__(self):
        return '<id %r>' % self.id


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/form', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['email'] and request.form['dist'] and (not request.form['dist'] == "District"):
            email = request.form['email']
            dist = request.form['dist']
            age = request.form['age']
            dose = request.form['dose']
            user = userData(email, dist, age, dose)
            try:
                db.session.add(user)
                db.session.commit()
                flash("You will be notified")
                return redirect(url_for('index'))
            except exc.IntegrityError:
                db.session.rollback()
                flash("Email id already registered")
                return redirect(url_for('index'))
        else:
            flash("Please enter valid details")
            return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
