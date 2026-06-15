import os
from flask import Flask, render_template
from dotenv import load_dotenv
from routes.dashboard import dashboard_bp
from routes.products import products_bp
from routes.management import management_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key-storage-management")

BACKEND_URL = os.getenv("BACKEND_URL", "")

@app.context_processor
def inject_backend_url():
    return dict(backend_url=BACKEND_URL)


app.register_blueprint(dashboard_bp)
app.register_blueprint(products_bp)
app.register_blueprint(management_bp)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
