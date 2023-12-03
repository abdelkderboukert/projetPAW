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