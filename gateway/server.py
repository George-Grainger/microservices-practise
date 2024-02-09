import os
import gridfs
import pika
import json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_service import access
from storage import util

server = Flask(__name__)
mongo = PyMongo(server, uri="mongodb://host.minikube.internal:27017/videos")

# Enables us to use https://www.mongodb.com/docs/manual/core/gridfs/
fs = gridfs.GridFS(mongo.db)

# Synchronous connection with RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def upload():
    access_json, err = validate.token(request)
    access_obj = json.loads(access_json)

    if access_obj["admin"]:
        if len(request.files) != 1:
            return "exactly 1 file required", 400

        # Should only be one file so should only happen once
        f = request.files.values()[0]
        err = util.upload(f, fs, channel, access_obj)

        if err:
            return err
        else:
            return "success", 200
    else:
        return "not authorized", 401


@server.route("/download", methods=["GET"])
def download():
    pass


if __name__ == "__main__":
    server.run(host="0.0.0.0", port="8080")
