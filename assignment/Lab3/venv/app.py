from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


#create extension
db= SQLAlchemy()

#create the app
app = Flask(__name__)

#configure the MYSQL db, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@host:port/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import terms
db.init_app(app)

# initialize the app with the extension  db.init_app(app)
db.init_app(app)

@app.get('/terms')
def get_terms():    
    t = db.session.query(terms).with_entities(terms.terms_id, terms.terms_description, terms.terms_due_days)
    ls=[]
    for v in t:        
        te = {            
              "id" : v.terms_id,            
              "description" : v.terms_description,            
              "due_days" : v.terms_due_days        
              }        
        ls.append(te)    
        return ls
@app.get('/terms1')
def get_terms1():
    t = db.session.query(terms).with_entities(terms.terms_id, terms.terms_description, terms.terms_due_days)
    lst = [v._asdict() for v in t]
    return lst
    
    app.run(host='127.0.0.1',port=5000)