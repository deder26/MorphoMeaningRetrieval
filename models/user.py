from database import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), unique=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
