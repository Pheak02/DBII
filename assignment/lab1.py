from flask import Flask, jsonify, request

app = Flask(__name__)

#Dic in classes
classes = [
    {
        "class": "M1",
        "student": [
            {'name': 'Sopheak', 'gender': 'F',},
            {'name': 'Dara', 'gender': 'M',},
            {'name': 'Thida', 'gender': 'F',},
            {'name': 'Monineath', 'gender': 'F',},
            {'name': 'Reaksa', 'gender': 'M',},  
        ]
    },
    {
        "class": "M2",
        "student": [
            {'name': 'Mony', 'gender': 'F',},
            {'name': 'Vireak', 'gender': 'M',},
            {'name': 'Many', 'gender': 'F',},
            {'name': 'Jnint', 'gender': 'F',},
            {'name': 'Phai', 'gender': 'M',},  
        ]
    }
     
]

@app.route("/")
def home():
    return "Home"
@app.route('/api/lab1/classes', methods=['GET'])
def get_classes():
    return jsonify(classes)
# @app.route('/api/lab1/classes', methods=['POST'])
# def add_classes():
#     add_member_to_class = request.get_json()
#     classes.append(add_member_to_class)
#     return jsonify({'message':'Added member(s) to class sucessfully'})

if __name__ == '__main__':
    app.run()