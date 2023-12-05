from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from waitress import serve
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField
from wtforms.validators import DataRequired, equal_to, Length
from flask_bcrypt import Bcrypt  # Import Bcrypt
from flask_login import UserMixin, login_user, login_manager, logout_user, login_required, current_user, login_remembered,LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from wtforms.widgets import TextArea
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = '5511467d654732b6d9875da2691f78fd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # Initialize Bcrypt
# flask_login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
scheduler = APScheduler()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def valid(id, k):
    todo = to_do.query.get_or_404(id)
    todo.title = k
    db.session.commit()
    pass
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
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_to_do = db.Column(db.DateTime, nullable=False)
    hour_to_do = db.Column(db.String(2), nullable=False)
    min_to_do = db.Column(db.String(2), nullable=False)
    val = db.Column(db.String(10))

    def __repr__(self):
        return '<name %r>' % self.name


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
    hour_to_do = StringField("hour_to_do", validators=[DataRequired()])
    min_to_do = StringField("min_to_do", validators=[DataRequired()])
    checkbox = BooleanField("check if you do it")
    submit = SubmitField('create')

class searchForm(FlaskForm):
    search = StringField("search", validators=[DataRequired()])
    submit = SubmitField('search')

@app.route('/')
@login_required
def home():
    daily = to_do.query.order_by(to_do.date_to_do)
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('home.html',daily=daily, date=date)

@app.route('/login', methods=['POST', 'GET'])#done
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
                return render_template('login.html', form = form)
        
    else :
      return render_template('login.html', form = form)
    
@app.route('/add_user', methods = ['POST' , 'GET'])#done
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

@app.route('/logout', methods = ['GET', 'POST'])#done
@login_required
def log_out():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add-daily', methods = ['GET', 'POST'])
@login_required
def add_daily():
    form = todoForm()

    if form.validate_on_submit():
        new_task = to_do(title=form.title.data)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('add_daily'))

    tasks = to_do.query.all()
    return render_template('add_daily.html', form=form, tasks=tasks)

@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = to_do.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('todo'), url_for('add_daily'))

@app.route('/profil', methods = ['GET','POST'])#done
@login_required
def profil():
    i = 0
    j = 0
    dailys = User.query.all()#don't forget to make it to_do.query when u finished database problems
    for daily in dailys:
        if daily.name == 'admin1':# this one tow
            i = i + 1
        j = j + 1
    num = round(100 / (i * j))
    return render_template('profil.html', num = num, i = i, j = j)

@app.route('/arvhive', methods = ['GET', 'POST'])
@login_required
def archive():
    form = searchForm()
    dailys = to_do.query
    form1 = todoForm()
    if form.validate_on_submit():
        posts_shearch = form.search.data
        dailys = dailys.filter(to_do.title.like('%'+ posts_shearch + '%'))
        dailys = dailys.order_by(to_do.date_to_do)

    return render_template('archive.html', form=form, dailys=dailys, form1=form1)

@app.route('/todo', methods = ['GET','POST'])
@login_required
def todo():
    form = searchForm()
    dailys = to_do.query
    if form.validate_on_submit():
        posts_shearch = form.search.data
        dailys = dailys.filter(to_do.title.like('%'+ posts_shearch + '%'))
        dailys = dailys.order_by(to_do.date_to_do)

    return render_template('todo.html', form=form, dailys=dailys)

@app.route('/test', methods = ['GET','POST'])
@login_required
def test():
    return render_template('test.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    scheduler.add_job(id='valid', func=valid, trigger='interval', args=[1, 2], minutes=10)
    scheduler.start()
    serve(app, host='0.0.0.0', port=8080)
