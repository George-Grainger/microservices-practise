import jwt
import datetime
import os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config - variables used to connect to MQSQL databse
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "invalid credentials", 401

    # Check DB for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    # User not found in DB
    if res <= 0:
        return "invalid credentials", 401

    user_row = cur.fetchone()
    email = user_row[0]
    password = user_row[1]

    if auth.username != email or auth.password != password:
        return "invalid credentials", 401
    else:
        return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)


@server.route("/validate", method=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "invalid credentials", 401

    # Not checking if authorization type is bearer
    # Would want to do this in production app
    encoded_jwt = encoded_jwt.split(" ")

    try:
        decoded = jwt.decode(encoded_jwt, os.environ.get(
            "JWT_SECRET"), algorithm=["HS256"])
    except:
        return "not authorized", 403

    return decoded, 200


def createJWT(username, secret, authz):
    # Can use JWT to make requests to API - admin gives access to all endpoints
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.utcnow(),
            "admin": authz,
        },
        secret,
        algorithm="HS256"
    )


if __name__ == "__main__":
    # Default for host is localhost - requests wouldn't reach flask app
    server.run(host="0.0.0.0", port="5000")
