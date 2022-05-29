from app import app
from flask import jsonify


@app.route("/")
def ip():
    from socket import gethostbyname, getfqdn
    ip_user = gethostbyname(getfqdn())
    return jsonify(ip_user=ip_user)
