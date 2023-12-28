from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from models import terms, invoices  # Correct the import statement for the model

#create extension
db = SQLAlchemy()

#create the app
app = Flask(__name__)

#configur the MySql db, relative to the app instance folder     
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:meisme2023!@host:3306/create_db_ap'  
# app.config['SQLALCHEMY_DATABASE_URI'] ='http://sopheaksaing.iceteag8m5.click/index.php?route=/database/structure&db=ap_sopheak'  
  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize the SQLAlchemy extension with the Flask app
db.init_app(app)
#create the app
@app.get('/terms')
def get_terms():
    t = db.session.query(terms).with_entities(terms.terms_id, terms.terms_description, terms.terms_due_days)
    ls=[]
    for v in t:
        te = {
            "id": v.terms_id,
            "description": v.terms_description,
            "due_days": v.terms_due_days,
        }
        ls.append(te)
    return ls

@app.get('/terms1')
def get_terms1():
    t = db.session.query(terms).with_entities(terms.terms_id, terms.terms_description, terms.terms_due_days)
    lst = [v._asdict() for v in t]
    return lst

# to add a new term to the terms table
@app.post('/terms')
def post_terms():   
    try:        
        request_data = request.get_json()
        t = terms(terms_description = request_data["terms_description"],         
        terms_due_days = request_data["terms_due_days"])        
        
        db.session.add(t)        
        db.session.commit()        
        return {'message':'success'}, 201    
    except Exception as e:            
            print (e)            
            return {'message': 'Something went wrong!'}, 500

# update specific term information basedon the term_description
@app.put('/terms/<string:des>')
def put_terms(des):    
    request_data = request.get_json()    
    t = db.session.query(terms).filter(terms.terms_description==des).first()
        
    if t:        
        t.terms_description = request_data["terms_description"],        
        t.terms_due_days = request_data["terms_due_days"]        
        try:            
            db.session.commit()            
            return {'message':'Success'}        
        except exc.SQLAlchemyError as e:            
            return {'message': str(e.__cause__)}    
    else:        
        return {'message':'There is no record'},400
    

# retrieving specific terms from thedatabase.
@app.get('/terms/<int:id>')
def get_term(id):
    t = db.session.query(terms).with_entities(terms.terms_id,terms.terms_description, terms.terms_due_days).filter(terms.terms_id == id)
    lst = [v._asdict() for v in t]
    return lst

# retrieve all invoices with specific termsfrom the database.
@app.get('/invoices/term/<int:term_id>')
def get_invoices_term(term_id):
    inv = db.session.query(invoices, terms).join(terms, terms.terms_id == invoices.terms_id).with_entities(invoices.invoice_number, terms.terms_description).filter(invoices.terms_id == term_id).all()
    lst = [v._asdict() for v in inv]    
    return lst

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)