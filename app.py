from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from waitress import serve
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt  # Import Bcrypt
from flask_login import UserMixin, login_user, login_manager, logout_user, login_required, current_user, login_remembered
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = '5511467d654732b6d9875da2691f78fd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # Initialize Bcrypt
#the module
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    neme = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<name %r>' % self.name

#the forms
class userForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()]) 
    submit = SubmitField('login') 

class loginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()]) 
    submit = SubmitField('login')     
    
@app.route('/')
def home():
    name = "moh"
    return render_template('home.html', name= name)

@app.route('/login', methods=['POST', 'GET'])
def login():
    email = None 
    password = None
    form=loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None :
            form.password.data = ''
            form.email.data = ''
            flash(" this account does not exist")
            return render_template('login.html', email = email, password = password, form = form)
        else :
            return render_template('home.html')
        
    else :
      return render_template('login.html', email = email, password = password, form = form)

@app.route('/add_user', methods = ['POST' , 'GET'])
def add_user():
    name = None
    form = userForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(name=form.name.data, email=form.email.data, password_hash=form.password.data)
            db.session.add(user)
            db.session.commit()

            flash("welcome on our website")
            return render_template('home.html')
        else :
            flash("this accont already exist please try to login")
            return render_template('login.html')     
    else :
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password.data = ''
        return render_template('add_user.html',
                               form = form,
                               name = name)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        db.session.commit()
    
    serve(app, host='0.0.0.0', port=8080)
