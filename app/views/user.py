import jinja2
from flask import jsonify, request, Blueprint
from jinja2 import Environment, PackageLoader, select_autoescape

from models import User

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route("/", methods=["GET"])
def get_users():
    users = User.list()
    env = Environment(
        loader=PackageLoader("app"),
        autoescape=select_autoescape()
    )
    template = env.get_template("users.html")

    result = template.render(users=[u.to_dict() for u in users])
    return result


@users_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    user = User.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    return jsonify(user.to_dict())


@users_bp.route("/", methods=["POST"])
def create_user():
    if not (request.json and request.json.get("password")
            and request.json.get("birthday") and request.json.get("name")):
        return jsonify({"message": 'Please, provide "birthday", "name" and "password" in body.'}), 400

    name = request.json["name"]

    if User.find_by_name(name):
        return {"message": "User already exists"}

    new_user = User(**request.json).save()

    return jsonify(new_user.to_dict()), 201


@users_bp.route("/<user_id>", methods=["PATCH"])
def update_user(user_id):
    birthday = request.json.get("birthday")
    name = request.json.get("name")
    password = request.json.get("password")

    user = User.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    if birthday:
        user.birthday = birthday
    if name:
        user.name = name
    if password:
        user.hashed_password = User.generate_hash(password)
    user.save()
    return jsonify(user.to_dict())


@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    count = User.delete(user_id)
    if count:
        return jsonify({"message": "Deleted"})
    return jsonify({"message": "Not found"}), 404
