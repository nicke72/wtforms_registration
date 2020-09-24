from wtforms import SubmitField,SelectField, BooleanField, StringField, PasswordField, validators
from flask_wtf import Form
from datetime import date, timedelta


class RegForm(Form):
    u = date.today()
    d = timedelta(14)
    t1 = u + timedelta(7)
    t2 = u + timedelta(14)
    t3 = u + timedelta(21)
    mac_address = StringField('Mac Address', [validators.DataRequired(), validators.MacAddress()])
    #name_last = StringField('Last Name', [validators.DataRequired()])
    date_expired = SelectField('Choose Expiration date', choices=[(str(t1), str(t1)), (str(t2), str(t2)), (str(t3), str(t3))])
    email = StringField('Email Address', [validators.DataRequired(), validators.Email(), validators.Length(min=6, max=35)])
    
    submit = SubmitField('Submit')

class loginForm(Form):
    email = StringField('Email', [validators.DataRequired(), validators.Email(), validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Submit')


