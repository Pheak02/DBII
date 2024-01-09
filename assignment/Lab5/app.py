from flask import Flask
from flask_restx import Api, Resource, reqparse
from sqlalchemy import exc
from config import Config
from models import terms
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Terms, Users

config = Config()
app = Flask(__name__)
app.config.from_object(config)

# Initialize the Flask app context and create tables
with app.app_context():
    db.init_app(app)
    db.create_all()

api = Api(app, version='1.0', title='Your API', description='API Description')
api_ns = api.namespace("Reference", path='/apiv1', description="Reference Data")


put_users_parser = reqparse.RequestParser()
put_users_parser.add_argument('username', type=str, required=True, help='Username is required')
put_users_parser.add_argument('password', type=str, required=True, help='Password is required')


@api_ns.route('/register')
class ManageUser(Resource):    
    @api.expect(put_users_parser)
    def post(self):
        args = put_users_parser.parse_args()
        username = args['username']
        password = args['password']
        user = Users.query.filter_by(username=username).first()
        if user:
            return {'message': 'User already exists'}, 400
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201
@api_ns.route('/login')
class UserLogin(Resource):
    @api.expect(put_users_parser)
    def post(self):
        args = put_users_parser.parse_args()
        username = args['username']
        password = args['password']
        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return {'message': 'Successfully logged in'}, 200
        return {'message': 'Invalid username or password'}, 401
# Define a data model for output marshalling
terms_fields = api.model('Terms', {
    'terms_description': fields.String(description='The terms description'),
    'terms_due_days': fields.Integer(description='The terms due days')})
# Define a data model for input
put_terms_parser = reqparse.RequestParser()
put_terms_parser.add_argument('terms_description', type=str, required=True, help='Terms description is required')
put_terms_parser.add_argument('terms_due_days', type=int, required=True, help='Terms due days is required')
@api_ns.route('/terms')
class AllTermsResource(Resource):
    def get(self):
        terms = db.session.query(Terms).all()
        return [{'terms_id': term.terms_id, 'terms_description': term.terms_description, 'terms_due_days': term.terms_due_days} for term in terms]
@api_ns.route('/terms/<int:id>')
class GetTerm(Resource):
    @api_ns.marshal_with(terms_fields)
    def get(self, id):
        term = db.session.query(Terms).filter_by(terms_id=id).first()
        if term:
            return term
        return {'message': 'Term not found'}, 404
    @api.expect(put_terms_parser)
    @api_ns.marshal_with(terms_fields)
    def put(self, id):
        args = put_terms_parser.parse_args()
        term = db.session.query(Terms).filter_by(terms_id=id).first()
        if term:
            term.terms_description = args['terms_description']
            term.terms_due_days = args['terms_due_days']
            try:
                db.session.commit()
                return term
            except exc.SQLAlchemyError as e:
                return {'message': str(e.__cause__)}, 500
            else:            return {'message': 'Term not found'}, 404
@api.route('/swagger')
class SwaggerResource(Resource):
    def get(self):
        return api.swagger_ui()
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)