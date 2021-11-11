from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from budget.models import User


class RegistrationFrom(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('ایمیل', validators=[DataRequired()])
    password = PasswordField('رمز عبور', validators=[DataRequired()])
    confirm_password = PasswordField('تایید رمز عبور', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('ثبت نام')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('نام کاربری یا ایمیل مورد نظر قبلا ثبت نام کرده است!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('نام کاربری یا ایمیل مورد نظر قبلا ثبت نام کرده است!')


class LoginForm(FlaskForm):
    email = StringField('ایمیل', validators=[DataRequired()])
    password = PasswordField('رمز عبور', validators=[DataRequired()])
    remember = BooleanField('به یاد بسپار')
    submit = SubmitField('ورود')


class UpdateProfileForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('ایمیل', validators=[DataRequired()])
    submit = SubmitField('بروزرسانی')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('نام کاربری یا ایمیل مورد نظر قبلا ثبت نام کرده است!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('نام کاربری یا ایمیل مورد نظر قبلا ثبت نام کرده است!')


class BuyForm(FlaskForm):
    price = IntegerField('مبلغ', validators=[DataRequired()])
    desc = StringField('توضیحات', validators=[DataRequired()])
    category = StringField('دسته بندی', default='سایر')
    date = DateField('تاریخ', default=datetime.today())
    submit = SubmitField('انتشار')


class FilterBox(FlaskForm):
    startdate = DateField('تاریخ شروع', default=datetime.today())
    enddate = DateField('تاریخ پایان', default=datetime.today() + relativedelta(months=+1))
    submit = SubmitField('تایید')
