from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:123456789@localhost:3306/apdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import terms
db.init_app(app)

with app.app_context():
    db.create_all()


@app.get('/terms')
def get_terms1():
    t = db.session.query(terms)\
        .with_entities(terms.terms_id, terms.terms_description, terms.terms_due_days)
    lst = [v._asdict() for v in t]
    return lst

# @app.get('/terms/<int:id>')
# def get_term(id):
#     t = db.session.query(terms)\
#         .with_entities(terms.terms_id,terms.terms_description, terms.terms_due_days)\
#         .filter(terms.terms_id == id)
#     lst = [v._asdict() for v in t]
#     return lst

# @app.put('/terms/<string:des>')
# def put_terms(des):
#     request_data = request.get_json()

#     t = db.session.query(terms).filter(terms.terms_description==des).first()
    
#     if t:
#         t.terms_description = request_data["terms_description"],
#         t.terms_due_days = request_data["terms_due_days"]
#         try:
#             db.session.commit()
#             return {'message':'Success'}
#         except exc.SQLAlchemyError as e:
#             return {'message': str(e.__cause__)}
#     else:
#         return {'message':'There is no record'},400

if __name__=='__main__':
    app.run(host='127.0.0.1',port=5000)

