from flask import FLask

#initalize the flask application 
app = Flask(__name__)
companies = [
    {
        "name": "ABSARA",
        "items": [
            {
                "name": "pen",
                "price": 15.99
            },
            {
                "name": "book",
                "price": 11
            }
        ]
    }
]
@app.get("/test") #Get return value
def test():
    return {"msg":"hello world"} #keyvaue msg

@app.get("/companies")
def companies():
    return{"companies": companies}

@app.post("/companies") #can be the same url if method are difference, post to create new ele
def createNewItem():
    new_company ={"name": "Pheak's bookstore", "items":[]}
    companies.append(new_company)
    return {"msg": "Bravo!"}

if __name__ == '__main__':
    app.run(debug==True)
    
    #status 200 - success, 302 - err link, 401 - unauthorized, 404 - not found!