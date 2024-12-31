from flask_wtf import FlaskForm  
from wtforms import StringField, PasswordField, SubmitField, BooleanField  
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  
from flaskblog.models import User  

class RegistrationForm(FlaskForm):  # 建立註冊表單類別
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])  # 使用者名稱欄位，限制 2~20 字元，必填
    email = StringField('Email', validators=[DataRequired(), Email()])  # 電子郵件欄位，檢查格式，必填
    password = PasswordField('Password', validators=[DataRequired()])  # 密碼欄位，必填
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])  # 確認密碼欄位，必填且需與密碼一致
    submit = SubmitField('Sign Up')  # 提交按鈕

    def validate_username(self, username):  # 自訂驗證方法，檢查使用者名稱是否已存在
        user = User.query.filter_by(username=username.data).first()  # 從資料庫查找是否有相同的使用者名稱
        if user:  # 如果找到重複的使用者名稱
            raise ValidationError('That username is taken. Please choose a different one.')  # 拋出驗證錯誤訊息

    def validate_email(self, email):  # 自訂驗證方法，檢查電子郵件是否已存在
        user = User.query.filter_by(email=email.data).first()  # 從資料庫查找是否有相同的電子郵件
        if user:  # 如果找到重複的電子郵件
            raise ValidationError('That email is taken. Please choose a different one.')  # 拋出驗證錯誤訊息

class LoginForm(FlaskForm):  # 建立登入表單類別
    email = StringField('Email', validators=[DataRequired(), Email()])  # 電子郵件欄位，檢查格式，必填
    password = PasswordField('Password', validators=[DataRequired()])  # 密碼欄位，必填
    remember = BooleanField('Remember Me')  # 記住我選項 布林值
    submit = SubmitField('Login')  # 提交按鈕
