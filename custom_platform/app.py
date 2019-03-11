import os, sys
import boto3
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask import session
from custom_platform.model.user import User, UserSchema
from functools import wraps

app = Flask(__name__)

try:
    USERS_TABLE = os.environ["USERS_TABLE"]
except KeyError:
    USERS_TABLE = "users-table-dev"

client = boto3.client("dynamodb")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid Credentials. Please try again."
        else:
            return redirect(url_for("home"))
    return render_template("login.html", error=error)


u = User("1","myname","somepassw","admin") # mock user

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if u.get_current_user_role() not in roles:
                return u.error_response()
            return f(*args, **kwargs)
        return wrapped
    return wrapper


@app.route("/")
@requires_roles("admin", "user", "guest")
def home():
    return "Lambda Serverless Stack"


@app.route("/welcome")
@requires_roles("admin", "user", "guest")
def welcome():
    if not session.get("access"):
        return redirect(url_for("login"))

    return render_template("welcome.html")


@app.route("/users/<string:user_id>", methods=["GET"])
@requires_roles("admin", "user")
def get_user(user_id):
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            "user_id": {"S": user_id}
        }
    )
    item = resp.get("Item")
    if not item:
        return jsonify({"error": "User does not exist"}), 404

    return jsonify({
        "user_id": item.get("user_id").get("S"),
        "name": item.get("name").get("S"),
        "access": item.get("access").get("S")
    })


@app.route("/users", methods=["POST"])
@requires_roles("admin", "user")
def create_user():
    schema = UserSchema()
    new_user = schema.dump(request.get_json())
    print(new_user)
    if not new_user["user_id"] or not new_user.get("name"):
        return jsonify({"error": "Please provider user_id and name"}), 400

    try:
        resp = client.put_item(
            TableName=USERS_TABLE,
            Item={
                "user_id": {"S": new_user.get("user_id")},
                "name": {"S": new_user.get("name")},
                "password": {"S": new_user.get("password")},
                "access": {"S": new_user.get("access")}
            }
        )
    except Exception:
        return jsonify({"The following issue occurred while creating": "{}".format(sys.exc_info()[0])}), 400

    return jsonify({
        "user_id": new_user.get("user_id"),
        "name": new_user.get("name"),
        "access": new_user.get("access")
    })


@app.route("/users/<string:user_id>", methods=["PUT"])
@requires_roles("admin", "user")
def update_user(user_id):
    schema = UserSchema()
    fields_to_update = schema.dump(request.get_json())
    print(fields_to_update)

    # put_item() will update item if exists, otherwise create new item
    try:
        client.put_item(
            TableName=USERS_TABLE,
            Item={
                "user_id": {"S": user_id},
                "name": {"S": fields_to_update.get("name")},
                "password": {"S": fields_to_update.get("password")},
                "access": {"S": fields_to_update.get("access")}
            }
        )
    except Exception as e:
        return jsonify({"The following issue occurred while updating": str(e)}), 400

    return jsonify({"User updated successfully. User ID ": user_id})


@app.route("/users/<string:user_id>", methods=["DELETE"])
@requires_roles("admin")
def delete_user(user_id):
    try:
        client.delete_item(
            TableName=USERS_TABLE,
            Key={
                "user_id": {"S": user_id}
            }
        )
    except Exception as e:
        return jsonify({"The following issue occurred while updating": str(e)}), 400

    return jsonify({"User deleted. User ID ": user_id}), 200


if __name__ == "__main__":
    app.run(debug=True)

