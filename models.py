from app import db  # app.py から db をインポート

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
    
class External_data(db.Model):
    __tablename__ = 'external_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<External_data {self.first_name} {self.last_name}>"
    

class Validateuser(db.Model):
    __tablename__ = 'user_role'

    username = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    userrole = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Validateuser {self.username}>'
    
    @staticmethod
    def validate_user(username):
        # ユーザー名でユーザーを検索
        user = Validateuser.query.filter_by(username=username).first()
        if user:
            return user  # ユーザーが見つかればそのユーザーを返す
        return None  # 見つからなければNoneを返す