from flask import render_template, url_for, flash, redirect, request  
from flaskblog import app, db, bcrypt  
from flaskblog.forms import RegistrationForm, LoginForm  
from flaskblog.models import User, Post  
from flask_login import login_user, current_user, logout_user, login_required  

# 範例文章資料，模擬用於主頁顯示
posts = [
    {
        'author': '5B0G0022',  # 文章作者
        'title': 'Blog Post 1',  # 文章標題
        'content': 'First post content',  # 文章內容
        'date_posted': 'December 30, 2024'  # 發佈日期
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'December 31, 2024'
    }
]

@app.route("/")  # 定義首頁路由
@app.route("/home")  # 定義 /home 路由，與首頁共用同一視圖
def home():
    return render_template('home.html', posts=posts)  # 渲染 home.html 模板，並傳遞文章資料給模板

@app.route("/about")  # 定義 /about 路由
def about():
    return render_template('about.html', title='About')  # 渲染 about.html 模板，並傳遞標題 'About'

@app.route("/register", methods=['GET', 'POST'])  # 定義 /register 路由，支援 GET 與 POST 請求
def register():
    if current_user.is_authenticated:  # 如果使用者已登入，重導向到首頁
        return redirect(url_for('home'))
    form = RegistrationForm()  # 建立註冊表單實例
    if form.validate_on_submit():  # 驗證表單提交的數據
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # 將密碼加密
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)  # 建立新的使用者實例
        db.session.add(user)  # 將新使用者加入資料庫會話
        db.session.commit()  # 提交變更
        flash('Your account has been created! You are now able to log in', 'success')  # 顯示成功訊息
        return redirect(url_for('login'))  # 重導向到登入頁面
    return render_template('register.html', title='Register', form=form)  # 渲染 register.html 模板，傳遞表單實例

@app.route("/login", methods=['GET', 'POST'])  # 定義 /login 路由，支援 GET 與 POST 請求
def login():
    if current_user.is_authenticated:  # 如果使用者已登入，重導向到首頁
        return redirect(url_for('home'))
    form = LoginForm()  # 建立登入表單實例
    if form.validate_on_submit():  # 驗證表單提交的數據
        user = User.query.filter_by(email=form.email.data).first()  # 根據電子郵件查詢使用者
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # 檢查使用者是否存在且密碼正確
            login_user(user, remember=form.remember.data)  # 登入使用者，根據表單選項設置是否記住
            next_page = request.args.get('next')  # 獲取重導向目標（如果存在）
            return redirect(next_page) if next_page else redirect(url_for('home'))  # 重導向到目標頁面或首頁
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')  # 顯示失敗訊息
    return render_template('login.html', title='Login', form=form)  # 渲染 login.html 模板，傳遞表單實例

@app.route("/logout")  # 定義 /logout 路由
def logout():
    logout_user()  # 登出使用者
    return redirect(url_for('home'))  # 重導向到首頁

@app.route("/account")  # 定義 /account 路由
@login_required  # 確保使用者必須登入才能訪問
def account():
    return render_template('account.html', title='Account')  # 渲染 account.html 模板，傳遞標題 'Account'
