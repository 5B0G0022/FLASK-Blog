from datetime import datetime  
from flaskblog import db, login_manager  
from flask_login import UserMixin  

@login_manager.user_loader  # 註冊用於加載使用者的回呼函數
def load_user(user_id):  # 定義函數以根據使用者 ID 加載使用者
    return User.query.get(int(user_id))  # 從資料庫查詢並返回對應的 User 物件

class User(db.Model, UserMixin):  # 定義 User 類別，繼承資料庫模型和 UserMixin
    id = db.Column(db.Integer, primary_key=True)  # 使用者的唯一 ID，主鍵
    username = db.Column(db.String(20), unique=True, nullable=False)  # 使用者名稱，必須唯一且不可為空
    email = db.Column(db.String(120), unique=True, nullable=False)  # 電子郵件，必須唯一且不可為空
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # 頭像檔案名稱，預設為 'default.jpg'
    password = db.Column(db.String(60), nullable=False)  # 密碼，儲存加密後的字串
    posts = db.relationship('Post', backref='author', lazy=True)  # 與 Post 模型的關聯，一對多關係

    def __repr__(self):  # 定義如何以字串形式表示 User 物件
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"  # 返回使用者名稱、電子郵件和頭像檔案名稱

class Post(db.Model):  # 定義 Post 類別，繼承資料庫模型
    id = db.Column(db.Integer, primary_key=True)  # 貼文的唯一 ID，主鍵
    title = db.Column(db.String(100), nullable=False)  # 貼文標題，最多 100 字，且不可為空
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 發佈日期，預設為目前 UTC 時間
    content = db.Column(db.Text, nullable=False)  # 貼文內容，不可為空
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外鍵，關聯到 User 表的 ID 欄位，表示發佈者

    def __repr__(self):  # 定義如何以字串形式表示 Post 物件
        return f"Post('{self.title}', '{self.date_posted}')"  # 返回貼文標題和發佈日期
