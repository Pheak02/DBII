from flask import Flask
from flask_restx import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from config import Config
from models import terms
config = Config()
db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(config)
api = Api(app, version='1.0', title='Your API', description='API Description')
api_ns = api.namespace("Reference", path='/apiv1', description="Reference Data")
test_ns = api.namespace("Invoices", path='/inv', description="Invoices Data")
db.init_app(app)

with app.app_context():    
    db.create_all()

@test_ns.route('/test')
@api_ns.route('/terms')
class AllTermsResource(Resource):
    def get(self):
        t = db.session.query(terms).with_entities(terms.terms_id, terms.terms_description, terms.terms_due_days)
        lst = [v._asdict() for v in t]
        return lst
put_terms_parser = reqparse.RequestParser()
put_terms_parser.add_argument('terms_description', type=str, required=True, help='Terms description is required')
put_terms_parser.add_argument('terms_due_days', type=int, required=True, help='Terms due days is required')
@api_ns.route('/terms/<int:id>')
class GetTerm(Resource):
    def get(self, id):
        t = db.session.query(terms).with_entities(terms.terms_id, terms.terms_description, terms.terms_due_days).filter(terms.terms_id == id)
        lst = [v._asdict() for v in t]
        return lst
    @api.expect(put_terms_parser)
    def put(self, id):
        args = put_terms_parser.parse_args()
        t = db.session.query(terms).filter(terms.terms_id == id).first()
        if t:
            t.terms_description = args['terms_description']
            t.terms_due_days = args['terms_due_days']
            try:
                db.session.commit()
                return {'message': 'Success',
                        'terms_description': t.terms_description,
                        'terms_due_days': t.terms_due_days}
            except exc.SQLAlchemyError as e:
                return {'message': str(e.__cause__)}, 500
            else:            
                return {'message': 'There is no record'}, 400
@api.route('/swagger')
class SwaggerResource(Resource):
    def get(self):
        return api.swagger_ui()
if __name__ == '__main__':    app.run(host='127.0.0.1', port=5000, debug=True)