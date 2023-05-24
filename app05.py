from flask import Flask, render_template, abort
from blueprints.admin import routes

app = Flask(__name__)

# registracia BP
app.register_blueprint(routes.admin_bp)
@app.route("/")
@app.route("/index")

def index():
    return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True)

