from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from waitress import serve
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, equal_to, Length
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_bcrypt import Bcrypt  # Import Bcrypt
from flask_login import UserMixin, login_user, login_manager, logout_user, login_required, current_user, login_remembered,LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import datetime
from wtforms.widgets import TextArea
from flask_apscheduler import APScheduler
from flask_migrate import Migrate
from jinja2_time import TimeExtension
from validate_email import validate_email

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = '5511467d654732b6d9875da2691f78fd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
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

app.jinja_env.filters['datetime'] = datetime.datetime.strptime
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
    hour_to_do = db.Column(db.Integer, nullable=True, default=8)
    min_to_do = db.Column(db.Integer, nullable=True, default=00)
    val = db.Column(db.String(1))
    pre = db.Column(db.String(1))
    datenow = db.Column(db.DateTime, default=datetime.datetime.utcnow)

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
    date_to_do = DateField('date_to_do', format='%Y-%m-%d', validators=[DataRequired()])
    hour_to_do = StringField("hour_to_do", validators=[DataRequired()])
    min_to_do = StringField("min_to_do", validators=[DataRequired()])
    checkbox = BooleanField("check if you do it")
    submit = SubmitField('create')

class addForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    text = StringField("text", widget=TextArea())
    date_to_do = DateField('date_to_do', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.date.today())
    hour_to_do = StringField("hour_to_do", validators=[DataRequired()], default=8)
    min_to_do = StringField("min_to_do", validators=[DataRequired()], default=0)
    rep = StringField("rep", validators=[DataRequired()])
    dro = SelectField(u'Choose a programming language', choices=[
        (0, ''),
        (1, 'Highest'),
        (2, 'Medium'),
        (3, 'Normal'),
    ], render_kw={"placeholder": "Choose a priority"}, validators=[DataRequired()])
    submit = SubmitField('create')

class searchForm(FlaskForm):
    search = StringField("search", validators=[DataRequired()])
    submit = SubmitField('search')

@app.route('/')
@login_required
def home():
    daily = to_do.query.filter(to_do.id_user==current_user.id)
    search = request.form.get('search', '')
    result = to_do.query.filter(to_do.title.like(f'%{search}%')).all()
    current_date = datetime.datetime.now().date()
    current_hour = datetime.datetime.now().hour
    return render_template('home.html',daily=daily, hour= current_hour, date=current_date, result=result)

@app.route('/login', methods=['POST', 'GET'])#done
def login():
    form=loginForm()
    for i in enumerate(form):
        print(i[1].data)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        passed = check_password_hash(user.password_hash, form.password.data )
        if user is None or not passed :
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
        v = validate_email(form.email.data, verify=True)
        if v:
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
        else:
           form.email.data = ''
           return render_template('add_user.html',
                               form = form,
                               ) 
    else :
        return render_template('add_user.html',
                               form = form,
                               )

@app.route('/logout', methods = ['GET', 'POST'])#done
@login_required
def log_out():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add-daily', methods = ['GET', 'POST'])#done
@login_required
def add_daily():
    form = addForm()
    if form.validate_on_submit():
        if form.hour_to_do == '':
            form.hour_to_do= '8'
        if form.min_to_do == '':
            form.min_to_do= '00'
        
        k = int(form.rep.data)
        p = int(form.dro.data)
        hour = int(form.hour_to_do.data)
        min = int(form.min_to_do.data)
        while k != -1: 
          form.date_to_do.data = form.date_to_do.data + timedelta(days=k)
          new_task = to_do(title=form.title.data, date_to_do=form.date_to_do.data, hour_to_do=hour, min_to_do=min, text=form.text.data,id_user= current_user.id , pre=p, val=0)
          db.session.add(new_task)
          db.session.commit()
          k=k-1

        
        flash('Task added successfully!', 'success')
        return redirect(url_for('add_daily'))

    tasks = to_do.query.all()
    return render_template('add_daily.html', form=form, tasks=tasks)

@app.route('/delete/<int:task_id>')#done
@login_required
def delete_task(task_id):
    task = to_do.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('todo'))

@app.route('/profil', methods = ['GET','POST'])#done
@login_required
def profil():
    i = 0
    j = 0
    s = 0
    dailys = to_do.query.filter(to_do.id_user==current_user.id).all()
    if dailys != None:
        for daily in dailys:
          if daily.val == '0':
              i = i + 1
          j = j + 1
        
        if i != 0:
           num = round (1 /((i / j) / 100))
        else:
           num =0
    else:
        num = 0
    return render_template('profil.html', num = num, i = i, j = j)

@app.route('/arvhive', methods = ['GET', 'POST'])
@login_required
def archive():
    form = searchForm()
    dailys = to_do.query.filter(to_do.id_user==current_user.id)
    form1 = todoForm()
    search = request.form.get('search', '')
    result = to_do.query.filter(to_do.title.like(f'%{search}%')).all()
    current_date = datetime.datetime.now().date()
    current_hour = datetime.datetime.now().hour
    return render_template('archive.html', form=form, dailys=dailys, form1=form1, date= current_date, hour= current_hour, result=result)

@app.route('/todo', methods = ['GET','POST'])
@login_required
def todo():
    dailys = to_do.query.filter(to_do.id_user==current_user.id)
    search = request.form.get('search', '')
    result = to_do.query.filter(to_do.title.like(f'%{search}%')).all()
    current_date = datetime.datetime.now().date()
    current_hour = datetime.datetime.now().hour
    return render_template('todo.html', dailys=dailys, date= current_date, hour= current_hour, result=result)
    
@app.route('/test', methods=['GET','POST'])
@login_required
def test():

    return render_template('test.html')
    
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if query:
        # perform the search here
        results = to_do.query.filter(to_do.title.like(f'%{query}%')).all()
        current_date = datetime.datetime.now().date()
        current_hour = datetime.datetime.now().hour
        return render_template('archive.html', results=results, hour= current_hour, date = current_date)
    else:
        return "Please enter a search term."
    app.add_url_rule('/search', view_func=search, methods=['GET'])

@app.route('/search1', methods=['GET'])
def search1():
    query = request.args.get('query', '')
    if query:
        # perform the search here
        results = to_do.query.filter(to_do.title.like(f'%{query}%')).all()
        current_date = datetime.datetime.now().date()
        current_hour = datetime.datetime.now().hour
        return render_template('todo.html', results=results, hour= current_hour, date = current_date)
    else:
        return "Please enter a search term."
    app.add_url_rule('/search1', view_func=search, methods=['GET'])

@app.route('/search2', methods=['GET'])
def search2():
    query = request.args.get('query', '')
    if query:
        # perform the search here
        results = to_do.query.filter(to_do.title.like(f'%{query}%')).all()
        current_date = datetime.datetime.now().date()
        current_hour = datetime.datetime.now().hour
        return render_template('home.html', results=results, hour= current_hour, date = current_date)
    else:
        return "Please enter a search term."
    app.add_url_rule('/search2', view_func=search, methods=['GET'])
with app.app_context():
        db.create_all()

if __name__ == "__main__":


    #migrate = Migrate(app, db)
    scheduler.add_job(id='valid', func=valid, trigger='interval', args=[1, 2], minutes=10)
    scheduler.start()
    serve(app, host='0.0.0.0', port=8080)
 