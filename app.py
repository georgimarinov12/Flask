import json
import uuid

from flask import Flask
from flask import request
from flask import render_template

from model.ad import Ad
from model.user import User
from errors import register_error_handlers

from security.basic_authentication import generate_password_hash
from security.basic_authentication import init_basic_auth


app = Flask(__name__)
auth = init_basic_auth()
register_error_handlers(app)


@app.route("/api/ads", methods = ["POST"])
@auth.login_required
def create_ad():
    ad_data = request.get_json(force=True, silent=True)
    if ad_data == None:
        return "Bad request", 400
    ad = Ad(ad_data["title"], ad_data["desc"], ad_data["price"], ad_data["date"], ad_data["buyer"])
    ad.save()
    return json.dumps(ad.to_dict()), 201


@app.route("/api/ads", methods = ["GET"])
def list_ads():
    result = {"result": []}
    for ad in Ad.all():
        result["result"].append(ad.to_dict())
    return json.dumps(result)


@app.route("/api/ads/<ad_id>", methods = ["GET"])
def get_ad(ad_id):
    return json.dumps(Ad.find(ad_id).to_dict())


@app.route("/api/ads/<ad_id>", methods = ["DELETE"])
@auth.login_required
def delete_ad(ad_id):
    Ad.delete(ad_id)
    return ""


@app.route("/api/ads/<ad_id>", methods = ["PATCH"])
@auth.login_required
def change_ad(ad_id):
    ad_data = request.get_json(force=True, silent=True)
    if ad_data == None:
        return "Bad request", 400

    ad = Ad.find(ad_id)
    if "title" in ad_data:
        ad.title = ad_data["title"]
    if "desc" in ad_data:
        ad.content = ad_data["content"]
    if "price" in ad_data:
        ad.content = ad_data["price"]
    return json.dumps(ad.save().to_dict())


@app.route("/api/users", methods = ["POST"])
def create_user():
    user_data = request.get_json(force=True, silent=True)
    if user_data == None:
        return "Bad request", 400
    hashed_password = generate_password_hash(user_data["password"])
    user = User(user_data["username"], hashed_password, user_data["email"], user_data["address"], user_data["phone_number"])
    user.save()
    return json.dumps(user.to_dict()), 201


@app.route("/api/posts/<user_id>", methods = ["GET"])
def get_user(user_id):
    return json.dumps(User.find(user_id).to_dict()


@app.route("/api/users", methods = ["GET"])
def list_users():
    result = {"result": []}
    for user in User.all():
        result["result"].append(user.to_dict())
    return json.dumps(result)


@app.route("/api/users/<user_id>", methods = ["PATCH"])
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
    return json.dumps(post.save().to_dict())


@app.route("/api/users/<user_id>", methods = ["DELETE"])
def delete_user(user_id):
    User.delete(user_id)
    return ""


@app.route("/", methods = ["GET"])
@auth.login_required
def ads():
    return render_template("index.html")


@app.route("/ads/<ad_id>", methods = ["GET"])
def view_ad(ad_id):
    return render_template("ad.html", ad=Ad.find(ad_id))


