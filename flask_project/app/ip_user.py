from flask import jsonify
from app import app


@app.route("/ip")
def ip():
    from socket import gethostbyname, getfqdn
    ip_user = gethostbyname(getfqdn())
    return jsonify(ip_user=ip_user)
