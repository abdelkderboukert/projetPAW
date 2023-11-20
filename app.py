from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from waitress import serve
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, equal_to, Length
from flask_bcrypt import Bcrypt  # Import Bcrypt
from flask_login import UserMixin, login_user, login_manager, logout_user, login_required, current_user, login_remembered,LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from wtforms.widgets import TextArea

app = Flask(__name__)
app.config['SECRET_KEY'] = '5511467d654732b6d9875da2691f78fd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # Initialize Bcrypt
# flask_login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#the module
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
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

class to_do(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text)
    id_user = db.Column(db.String(5000000000), nullable=False)
    date_to_do = db.Column(db.DateTime)

#the forms
class userForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password_hash = PasswordField("password", validators=[DataRequired(), equal_to('password_hash2', message='password must match!')])
    password_hash2 = PasswordField("password", validators=[DataRequired()]) 
    submit = SubmitField('creat a new account') 

class loginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()]) 
    submit = SubmitField('login')     
    
class todoForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    text = StringField("text", widget=TextArea())
    date_to_do = StringField("date_to_do", validators=[DataRequired()])
    submit = SubmitField('create')

@app.route('/')
@login_required
def home():
    daily = to_do.query.order_by(to_do.date_to_do)
    return render_template('home.html',daily=daily)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form=loginForm()
    for i in enumerate(form):
        print(i[1].data)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        passed = check_password_hash(user.password_hash, form.password.data )
        if user is None :
            form.password.data = ''
            form.email.data = ''
            flash(" this account does not exist")
            return render_template('login.html', form = form)
        else :
            if passed is True :
                flash("login successful")
                login_user(user)
                return redirect(url_for('home'))
            else :
                flash("wrong password try again")
                form.password.data = ''
        
    else :
      return render_template('login.html', form = form)

@app.route('/add_user', methods = ['POST' , 'GET'])
def add_user():
    form = userForm()
    if form.validate_on_submit():
        print(form.email.data)
        user = User.query.filter_by(email=form.email.data).first()
        print('''user: {user}''')
        if user is None:
            #hash password!!
            hashed_pw = generate_password_hash(form.password_hash.data)
            user = User(name=form.name.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()

            flash("your account has been created please login ")
            return redirect(url_for('login'))
        else :
            flash("this accont already exist please try to login")
            return redirect(url_for('login'))     
    else :
        return render_template('add_user.html',
                               form = form,
                               )

@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add-daily', methods = ['GET', 'POST'])
def add_daily():
    form = todoForm()
    if form.validate_on_submit():
        todo = to_do(title=form.title.data, text=form.text.data, date_to_do=form.date_to_do.data)
        form.title.data = ''
        form.text.data = ''
        form.date_to_do.data = ''

        db.session.add(todo)
        db.session.commit()
        flash("submitted successfully")

    return render_template('add_daily.html', form=form)


@app.route('/profil', methods = ['GET','POST'])
@login_required
def profil():
    num = 60
    return render_template('profil.html', num = num)

@app.route('/arvhive', methods = ['GET', 'POST'])
def archive():
    return render_template('archive.html')

@app.route('/test', methods = ['GET','POST'])
def test():
    return render_template('test.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    serve(app, host='0.0.0.0', port=8080)
