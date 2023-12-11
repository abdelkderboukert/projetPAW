#class ToDo(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
 #   title = db.Column(db.String(50), nullable=False)
 #   text = db.Column(db.Text)
#    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#    date_to_do = db.Column(db.DateTime, nullable=False)

#    def __repr__(self):
#        return '<To Do %r>' % self.title

#def create_to_do(title, text, user_id, date_to_do):
#    to_do_entry = ToDo(title=title, text=text, user_id=user_id, date_to_do=date_to_do)
#    db.session.add(to_do_entry)
#    db.session.commit()

#def get_all_to_dos(user_id):
#    return ToDo.query.filter_by(user_id=user_id).all()

#def get_to_do(id):
#    return ToDo.query.get(id)

#def update_to_do(id, title, text, date_to_do):
#    to_do_entry = get_to_do(id)
#    to_do_entry.title = title
#    to_do_entry.text = text
#    to_do_entry.date_to_do = date_to_do
#    db.session.commit()

#def delete_to_do(id):
#    to_do_entry = get_to_do(id)
#    db.session.delete(to_do_entry)
#    db.session.commit()

#class ToDoForm(FlaskForm):
#    title = StringField("title", validators=[DataRequired()])
#    text = StringField("text", widget=TextArea())
#    date_to_do = StringField("date_to_do", validators=[DataRequired()])
 #   checkbox = BooleanField("check if you do it")
 #   submit = SubmitField('create')

#from datetime import datetime

#def add_daily(title, text, id_user, date_to_do, hour_to_do, min_to_do, val):
    #datenow = datetime.now()

    # convert strings to datetime objects
    #date_to_do = datetime.strptime(date_to_do, '%Y-%m-%d')
    #hour_to_do = datetime.strptime(hour_to_do, '%H').time()
    #min_to_do = datetime.strptime(min_to_do, '%M').time()

    # execute the query
    #db.session.add(ToDo(title=title, text=text, id_user=id_user, date_to_do=date_to_do, hour_to_do=hour_to_do, min_to_do=min_to_do, val=val, datenow=datenow))
    #db.session.commit()
              #{{ form.hidden_tag() }}{{ form.search(id="nav",
             # placeholder="search", autofocus=true) }}


from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from waitress import serve
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, DateField
from wtforms.validators import DataRequired, equal_to, Length
from flask_login import UserMixin, login_user, login_manager, logout_user, login_required, current_user, login_remembered,LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '5511467d654732b6d9875da2691f78fd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
# flask_login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    
#login form
class loginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()]) 
    submit = SubmitField('login')

#user form
class userForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password_hash = PasswordField("password", validators=[DataRequired(), equal_to('password_hash2', message='password must match!')])
    password_hash2 = PasswordField("password", validators=[DataRequired()]) 
    submit = SubmitField('creat a new account') 


# login route
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



 # add user route   
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
        <!-- {%block search%}
    <ul>
      <h2>Search Results</h2>
      <ul>
        {% for result in results %}
        <li>{{ result.title }}</li>
        {% endfor %}
      </ul>
      {% if not results %}
      <p>Please enter a search term.</p>
      {% endif %}
    {%endblock%}
      {% if date > result.date_to_do.date() %}
<div class="todo_con">
  <h3>{{ result.title }}</h3>
  <p class="hid" id="dat">{{ result.date_to_do.date() }}</p>
  <p class="hid" id="txt">{{ result.text }}</p>
  <p class="hid" id="hour">{{ result.hour_to_do }}</p>
  <p class="hid" id="datd">{{ result.datenow.date() }}</p>
</div>
{% endif %}{% endfor %}-->


           <div class="cherche">
            <!--<div class="#">
              {{ form.hidden_tag() }}{{ form.search(id="nav",
              placeholder="search", autofocus=true) }}
            </div>
            <button id="bt2">
              {{ form.hidden_tag() }}{{ form.submit(id="bt1") }}
            </button>
            <button class="drk">dark mode</button>
          </div>-->
background: linear-gradient(87deg, #F0F8FF 73%,#F65166 98%);zr9 7mr
background: linear-gradient(87deg, #F0F8FF 73%,#FF8C5B 98%);zr9 tchini     chevron_right    chevron_left