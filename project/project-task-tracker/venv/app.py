from flask import Flask
from flask_restx import Api, Resource, fields, reqparse
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:meisme2023!@localhost:3306/project_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app, version='1.0', title='Task Tracker API', description='API for managing project tasks')

db = SQLAlchemy(app)
# Model for task
task_model = api.model('Task', {
    'id': fields.String(readOnly=True, description='The task unique identifier'),
    'title': fields.String(required=True, description='Task title'),
    'description': fields.String(description='Task description'),
    'priority': fields.String(enum=['low', 'medium', 'high'], default='medium', description='Task priority'),
    'deadline': fields.String(description='Task deadline'),
    'assigned_to': fields.String(description='Assigned user'),
})

# Mock data
# tasks = [
#     {'id': '1', 'title': 'Task 1', 'description': 'Finish the course!', 'priority': 'high', 'deadline': '2024-01-01', 'assigned_to': 'Sopheak Saing'},
#     {'id': '2', 'title': 'Task 2', 'description': 'Can apply to real project', 'priority': 'medium', 'deadline': '2024-02-01', 'assigned_to': 'Sopheak Saing'},
# ]

class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    title = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(45))
    priority = db.Column(db.String(45), default='medium')
    deadline = db.Column(db.String(45))
    assigned_to = db.Column(db.String(45))

# Parser for request parameters
parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Task title')
parser.add_argument('description', type=str, help='Task description')
parser.add_argument('priority', type=str, choices=('low', 'medium', 'high'), help='Task priority')
parser.add_argument('deadline', type=str, help='Task deadline')
parser.add_argument('assigned_to', type=str, help='Assigned user')

# Resource for handling tasks
# @api.route('/tasks')
# class TaskListResource(Resource):
#     @api.marshal_list_with(task_model)
#     def get(self):
#         """List all tasks"""
#         return tasks

#     @api.expect(parser)
#     @api.marshal_with(task_model)
#     def post(self):
#         """Create a new task"""
#         args = parser.parse_args()
#         task = {'id': str(len(tasks) + 1), **args}
#         tasks.append(task)
#         return task, 201
@api.route('/tasks')
class TaskListResource(Resource):
    @api.marshal_list_with(task_model)
    def get(self):
        """List all tasks"""
        tasks = Task.query.all()
        return tasks

    @api.expect(parser)
    @api.marshal_with(task_model)
    def post(self):
        """Create a new task"""
        args = parser.parse_args()

        # Manually set the id using uuid
        args['id'] = str(uuid.uuid4())

        task = Task(**args)
        db.session.add(task)
        db.session.commit()
        return task, 201


@api.route('/tasks/<string:task_id>')
class TaskResource(Resource):
    @api.marshal_with(task_model)
    def get(self, task_id):
        """Get task details"""
        task = next((t for t in tasks if t['id'] == task_id), None)
        if task is None:
            api.abort(404, f"Task {task_id} not found")
        return task

    @api.expect(parser)
    @api.marshal_with(task_model)
    def put(self, task_id):
        """Update task"""
        task = next((t for t in tasks if t['id'] == task_id), None)
        if task is None:
            api.abort(404, f"Task {task_id} not found")

        args = parser.parse_args()
        task.update(args)
        return task

    def delete(self, task_id):
        """Delete task"""
        global tasks
        tasks = [t for t in tasks if t['id'] != task_id]
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)