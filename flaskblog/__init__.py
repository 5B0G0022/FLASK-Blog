from flask import Flask  
from flask_sqlalchemy import SQLAlchemy  # 匯入 SQLAlchemy，用於處理資料庫操作
from flask_bcrypt import Bcrypt  # 匯入 Bcrypt，用於處理密碼加密
from flask_login import LoginManager  

app = Flask(__name__)  # 建立 Flask 應用程式實例
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'  # 設置應用的秘密金鑰，用於保護數據
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # 配置資料庫 URI，使用 SQLite 資料庫

db = SQLAlchemy(app)  # 初始化 SQLAlchemy，綁定到 Flask 應用程式
bcrypt = Bcrypt(app)  # 初始化 Bcrypt，用於密碼哈希處理
login_manager = LoginManager(app)  # 初始化 LoginManager，綁定到 Flask 應用程式
login_manager.login_view = 'login'  # 設定登入頁面的路由名稱（'login' 是對應的視圖函數名稱）
login_manager.login_message_category = 'info'  # 設定閃現訊息的分類為 'info'，用於顯示提示訊息

with app.app_context():  # 自動初始化資料庫表
    db.create_all()  # 檢查並創建資料庫中的所有表（根據 models.py 定義）

from flaskblog import routes  
