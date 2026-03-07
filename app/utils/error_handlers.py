"""
Central error handlers for the Flask app.
Return consistent JSON for API errors and handle 404/500.
"""
from flask import jsonify


def register_error_handlers(app):
    """Register error handlers on the app."""

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request", "message": str(e)}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"error": "Unauthorized", "message": str(e)}), 401

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found", "message": "Resource not found"}), 404

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({"error": "Unprocessable entity", "message": str(e)}), 422

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error", "message": "An error occurred"}), 500
