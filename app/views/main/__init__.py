from flask import Blueprint, jsonify, request, url_for

bp = Blueprint("main", __name__)

@bp.route("/")
@bp.route('/main', methods=['GET', 'POST'])
def method_name():
    return jsonify({
        "message": "Welcome to ASOview API",
        "documentation": url_for('main.method_name', _external=True),
        "status": "OK"
    })