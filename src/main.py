import os
import sys
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///blacklist.db'

from src.db.database import init_db, create_tables
from src.routes.blacklist_router import blacklist_bp
from src.models.errors import BadRequestError, NotFoundError, ConflictError, UnauthorizedError

app = Flask(__name__)
CORS(app)
init_db(app)
with app.app_context():
    create_tables(app)

app.register_blueprint(blacklist_bp)

@app.errorhandler(BadRequestError)
def handle_bad_request(e):
    return jsonify({"error": "Bad Request", "message": str(e)}), 400

@app.errorhandler(NotFoundError)
def handle_not_found(e):
    return jsonify({"error": "Not Found", "message": str(e)}), 404

@app.errorhandler(ConflictError)
def handle_conflict(e):
    return jsonify({"error": "Conflict", "message": str(e)}), 409

@app.errorhandler(UnauthorizedError)
def handle_unauthorized(e):
    return jsonify({"error": "Unauthorized", "message": str(e)}), 401

@app.errorhandler(404)
def handle_flask_404(e):
    return jsonify({"error": "Not Found", "message": "The requested URL was not found"}), 404

@app.errorhandler(Exception)
def handle_generic_error(e):
    print(f"❌ Error: {e}")
    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    print("🚀 Iniciando servidor en http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)