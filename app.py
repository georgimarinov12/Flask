import json
import uuid

from flask import Flask
from flask import request
from flask import render_template, jsonify

from model.ad import Ad
from model.user import User
from errors import register_error_handlers

from security.basic_authentication import generate_password_hash
from security.basic_authentication import require_login, verify_password


app = Flask(__name__)
#auth = init_basic_auth()
register_error_handlers(app)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/ads", methods = ["POST"])
@require_login
def create_ad(user_id):
    ad_data = request.get_json(force=True, silent=True)
    if ad_data == None:
        return "Bad request", 400
    ad = Ad(user_id, ad_data["title"], ad_data["desc"], ad_data["price"], ad_data["date"], None, 1, None)
    ad.save()
    return json.dumps(ad.to_dict()), 201


@app.route("/ads", methods = ["GET"])
def list_ads():
    result = {"result": []}
    for ad in Ad.all():
        result["result"].append(ad.to_dict())
    return json.dumps(result)


@app.route("/api/ads/<ad_id>", methods = ["GET"])
def get_ad(ad_id):
    return json.dumps(Ad.find_by_id(ad_id).to_dict())


@app.route("/ads/<ad_id>", methods = ["DELETE"])
@require_login
def delete_ad(user_id, ad_id):
    ad_data = request.get_json(force=True, silent=True)
    if ad_data == None:
        return "Bad request", 400

    ad = Ad.find_by_id(ad_id)
    if ad.creator_id is not user_id:
        return "Forbidden", 403
    
    Ad.delete(ad_id)
    return ""


@app.route("/ads/<ad_id>", methods = ["PATCH"])
@require_login
def change_ad(user_id, ad_id):
    ad_data = request.get_json(force=True, silent=True)
    if ad_data == None:
        return "Bad request", 400

    ad = Ad.find_by_id(ad_id)
    if ad.creator_id is not user_id:
        print(ad.creator_id)
        print(user_id)
        return "Forbidden", 403
    
    if "title" in ad_data:
        ad.title = ad_data["title"]
    if "desc" in ad_data:
        ad.desc = ad_data["desc"]
    if "price" in ad_data:
        ad.price = ad_data["price"]
    return json.dumps(ad.save().to_dict())


@app.route("/ads/<ad_id>/buy", methods = ["PATCH"])
@require_login
def buy_article(user_id, ad_id):
    ad = Ad.find_by_id(ad_id)
    if ad.is_available == 0:
        return "Bad request", 400
    
    ad.is_available = 0
    ad.buyer = user_id
    
    return json.dumps(ad.save().to_dict())


@app.route("/register", methods = ["POST"])
def register():
    user_data = request.get_json(force=True, silent=True)
    if user_data == None:
        return "Bad request", 400
    hashed_password = generate_password_hash(user_data["password"])
    user = User(user_data["username"], hashed_password, user_data["email"], user_data["address"], user_data["phone_number"])
    user.save()
    return json.dumps(user.to_dict()), 201


@app.route("/login", methods = ["POST"])
def login():
    user_data = json.loads(request.data.decode('ascii'))
    email = user_data["email"]
    password = user_data["password"]
    user = User.find_by_email(email)
    
    if not user or not verify_password(email, password):
        return "Forbidden", 403
    token = user.generate_token()
    return jsonify({'token': token.decode('ascii')})


@app.route("/users/<user_id>", methods = ["GET"])
def get_user(user_id):
    return json.dumps(User.find(user_id).to_dict())


@app.route("/users", methods = ["GET"])
def list_users():
    result = {"result": []}
    for user in User.all():
        result["result"].append(user.to_dict())
    return json.dumps(result)


@app.route("/users/<user_id>", methods = ["PATCH"])
def change_user_info(user_id):
    user_data = request.get_json(force=True, silent=True)
    if user_data == None:
        return "Bad request", 400

    user = User.find(user_id)
    if "username" in user_data:
        user.username = user_data["username"]
    if "address" in user_data:
        user.address = user_data["address"]
    if "phone_number" in user_data:
        user.phone_number = user_data["phone_number"]
    return json.dumps(user.save().to_dict())


@app.route("/users/<user_id>", methods = ["DELETE"])
def delete_user(user_id):
    User.delete(user_id)
    return ""


@app.route("/users/purchased", methods = ["GET"])
@require_login
def list_purchased(user_id):
    return json.dumps(Ad.find_all_purchased(user_id))
    


@app.route("/ads/<ad_id>", methods = ["GET"])
def view_ad(ad_id):
    return render_template("ad.html", ad=Ad.find_by_id(ad_id))


if __name__ == '__main__':
    app.run()
