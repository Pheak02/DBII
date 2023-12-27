from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import terms

#create extension
db = SQLAlchemy()

#create the app
app = Flask(__name__)

#configur the MySql db, relative to the app instance folder     
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:meisme2023!@host:3306/create_db_ap'    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize the SQLAlchemy extension with the Flask app
from models import terms
db.init_app(app)

#create endpoint route
@app.get('/terms')
def get_terms():
    t = db.session.query(terms).with_entities(terms.terms_id, terms.terms_description, terms.terms_due_days  )
    ls=[]
    for v in t:
        te = {
            "id": v.terms_id,
            "description": v.terms_description,
            "due_days": v.term_due
        }
        ls.append(te)
        return ls
    
@app.get('/terms1')
def get_terms1():
    t=db.session.query(terms).with_entities(terms.terms.id, terms.terms.description, terms.terms.terms_due_days)
    lst=[v.asdict() for v in t]
    return lst
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)