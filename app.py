from datetime import datetime
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

# --------
#  Boomer
# --------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQLAlchemy(app)
api = Api(app)

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            abort(401, message="Not logged in")
        return fn(*args, **kwargs)
    return wrapper

# --------------------
#  Database Settings
# --------------------

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(80))
    last_week_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"User(username = {self.username}, hash = {self.hash})"
    
class WeekModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True) # Can be null
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)

class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ddl = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True) # YYYY-MM-DDTHH:MM:SS
    end_time = db.Column(db.DateTime, nullable=True)
    remark = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey('week_model.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category_model.id'), nullable=False)

class CategoryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), nullable=False) # Hex
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    
# ----------------------
#  User Authentication
# ----------------------
    
user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help="Username cannot be blank")
user_args.add_argument('password', type=str, required=True, help="Password cannot be blank")
user_args.add_argument('password_confirm', type=str, required=True, help="Confirm cannot be blank")

userFields = {
    'id':fields.Integer,
    'username':fields.String,
}

class Register(Resource):
    @marshal_with(userFields)
    def post(self):
        # register
        args = user_args.parse_args()
        if args['password'] != args['password_confirm']:
            abort(403, message="Confirmation failed!")
        user = UserModel(username=args["username"], hash=generate_password_hash(args["password"]))
        db.session.add(user)
        db.session.commit()
        return user, 201
    
login_args = reqparse.RequestParser()
login_args.add_argument('username', type=str, required=True)
login_args.add_argument('password', type=str, required=True)

class Login(Resource):
    def post(self):
        # login
        session.pop("user_id", None)
        args = login_args.parse_args()
        user = UserModel.query.filter_by(username=args['username']).first()
        if not user or not check_password_hash(user.hash, args['password']):
            abort(401, message="Invalid username or password")
        
        session['user_id'] = user.id
        return {"message": "Logged in successfully"}, 200
    
class Me(Resource):
    @login_required
    @marshal_with(userFields)
    def get(self):
        # Get user info      
        user_id = session.get('user_id')
        user = UserModel.query.get(user_id)
        return user
    
class Logout(Resource):
    @login_required
    @marshal_with(userFields)
    def post(self):
        # logout
        session.pop("user_id", None)
        return {"message": "Logged out successfully"}, 200

api.add_resource(Register, '/api/register/')
api.add_resource(Login, '/api/login/')
api.add_resource(Me, '/api/me/')
api.add_resource(Logout, '/api/logout/')

# ------------
#  Week Part
# ------------

week_args = reqparse.RequestParser()
week_args.add_argument('name', type=str, required=False, help="The name of the week")
week_args.add_argument('start_time', type=str, required=True, help="Start time cannot be blank")
week_args.add_argument('end_time', type=str, required=True, help="End time cannot be blank")

weekFields = {
    'id': fields.Integer,
    'name': fields.String,
    'start_time': fields.String,
    'end_time': fields.String
}

class CreateWeek(Resource):
    @login_required
    @marshal_with(weekFields)
    def post(self):
        # Create a new "week"
        user_id = session.get('user_id')
        args = week_args.parse_args()
        try:
            start_time = datetime.fromisoformat(args['start_time'])
            end_time = datetime.fromisoformat(args['end_time'])
        except ValueError:
            abort(400, message="Invalid datetime format")
        if end_time <= start_time:
            abort(400, message="End time must be later than start time")
        week = WeekModel(name=args['name'], start_time=start_time, end_time=end_time, user_id=user_id)
        db.session.add(week)
        db.session.commit()
        return week, 201
    
class ViewWeek(Resource):
    @login_required
    @marshal_with(weekFields)
    def get(self, week_id):
        # Get week info
        user_id = session.get('user_id')
        week = WeekModel.query.filter_by(id=week_id, user_id=user_id).first()
        if not week:
            abort(404, message="Week not found")
        # Remember "lastly_view"
        user = UserModel.query.get(user_id)
        user.last_week_id = week_id
        db.session.commit()
        return week
    
class LastView(Resource):
    @login_required
    def get(self):
        # Get the last week the user has ever viewed
        user_id = session.get('user_id')
        user = UserModel.query.get(user_id)
        if not user.last_week_id:
            # return {"last_week_id": None}
            abort(404, message="not found")
        return {"last_week_id": user.last_week_id}
    
class DeleteWeek(Resource):
    @login_required
    def delete(self, week_id):
        # Delete week
        user_id = session.get('user_id')
        week = WeekModel.query.filter_by(id=week_id, user_id=user_id).first()
        if not week:
            abort(404, message="Week not found")
        db.session.delete(week)
        db.session.commit()
        return {"message": "Week already been deleted"}, 200
    
api.add_resource(CreateWeek, '/api/week/create')
api.add_resource(ViewWeek, '/api/weeks/<int:week_id>')
api.add_resource(LastView, '/api/weeks/last')
api.add_resource(DeleteWeek, '/api/weeks/<int:week_id>')

# ------------
#  Task Part
# ------------

task_args = reqparse.RequestParser()
task_args.add_argument('title', type=str, required=True, help="Title cannot be blank")
task_args.add_argument('ddl', type=str, required=True, help="Deadline cannot be blank")
task_args.add_argument('start_time', type=str, required=False, help="Enter the start time")
task_args.add_argument('end_time', type=str, required=False, help="Enter the end time")
task_args.add_argument('category_id', type=str, required=True, help="Category cannot be blank")
task_args.add_argument('remark', type=str, required=False, help="Enter remark")
task_args.add_argument('week_id', type=str, required=True, help="Week id cannot be blank")

taskFields = {
    'id':fields.Integer,
    'title':fields.String,
    'ddl':fields.String,
    'start_time':fields.String,
    'end_time':fields.String,
    'category_id':fields.Integer,
    'remark':fields.String,
    'week_id':fields.Integer
}

class CreateTask(Resource):
    @login_required
    @marshal_with(taskFields)
    def post(self):
        # Create a task
        user_id = session.get('user_id')
        args = task_args.parse_args()
        try:
            ddl = datetime.fromisoformat(args['ddl'])
        except ValueError:
            abort(400, message="Invalid datetime format")
        task = TaskModel(
            title=args['title'],
            ddl=ddl,
            category_id=args['category_id'],
            remark=args['remark'],
            week_id=args['week_id'],
            user_id=user_id
        )
        db.session.add(task)
        db.session.commit()
        return task, 201
    
class SetTaskTime(Resource):
    @login_required
    @marshal_with(taskFields)
    def patch(self, task_id):
        # Set start time and end time for a task
        task_time_args = reqparse.RequestParser()
        task_time_args.add_argument('start_time', type=str, required=True, help="Start time is required")
        task_time_args.add_argument('end_time', type=str, required=True, help="End time is required")
                
        user_id = session.get('user_id')
        args = task_time_args.parse_args()
        task = TaskModel.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            abort(404, message="Task not found")
        try:
            task.start_time = datetime.fromisoformat(args['start_time'])
            task.end_time = datetime.fromisoformat(args['end_time'])
        except ValueError:
            abort(400, message="Invalid datetime format")
        db.session.commit()
        return task        

api.add_resource(CreateTask, '/api/task/create')
api.add_resource(SetTaskTime, '/api/task/<int:task_id>/time')

# -------------------
#  Call the Program
# -------------------

if __name__ == '__main__':
    app.run(debug=True)