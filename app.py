from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return f"User(username = {self.username}, hash = {self.hash})"
    
user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help="Username cannot be blank")
user_args.add_argument('password', type=str, required=True, help="Password cannot be blank")

userFields = {
    'id':fields.Integer,
    'username':fields.String,
}

class Users(Resource):
    @marshal_with(userFields)
    def post(self):
        # register
        args = user_args.parse_args()
        user = UserModel(username=args["username"], hash=generate_password_hash(args["password"]))
        db.session.add(user)
        db.session.commit()
        return user, 201
    

api.add_resource(Users, '/api/users/')

if __name__ == '__main__':
    app.run(debug=True)