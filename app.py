import os
import pymysql
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client.core import CollectorRegistry

from DBUtils.PersistentDB import PersistentDB

from metrics import load_metric_config_filename
from collector import BaseController
from exporter import metric_usage, baseRegistry, alphaRegistry

app = Flask(__name__)

@app.route("/")
def index():
    return "Index Page!"

@app.route("/hello")
def hello():
    return "Hello world!"

@app.route("/user/<username>")
def show_user_profile(username):
    return "User {username}".format(username=username)

@app.route('/metrics')
def show_metric():
    return "{}".format(metric_usage)

mysql_kwargs = dict(host="127.0.0.1",
                        port=3306,
                        user="root",
                        password="abcd1234")
mysql_client = PersistentDB(pymysql, **mysql_kwargs)

registries = {}

filenames = ["mariadb_version.yaml", "mariadb_test.yaml"]
for filename in filenames:
    mariadb_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", filename)
    query_config = load_metric_config_filename(mariadb_filename)
    current_collector = BaseController(query_config, mysql_client)
    current_endpoint = query_config.endpoint
    if not registries.get(current_endpoint):
        registries[current_endpoint] = CollectorRegistry()
    currentRegistry = registries.get(current_endpoint)
    currentRegistry.register(current_collector)

mount_path = {
    '/metrics/1s': make_wsgi_app(baseRegistry),
    '/metrics/10s': make_wsgi_app(alphaRegistry)
    }
for key, obj in registries.items():
    mount_path[key] = make_wsgi_app(obj)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, mount_path)