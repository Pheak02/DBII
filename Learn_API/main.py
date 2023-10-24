from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "Sopheak Saing",
        "email": "pheak@gmail.com"
    }
    extra = request.args.get('extra')
    if extra:
        user_data["extra"] = extra
    return jsonify(user_data), 200
# we created dic, with jsonify return dic to users, flask pass value
# set up application
if __name__ == "__main__":
    app.run(debug = True)