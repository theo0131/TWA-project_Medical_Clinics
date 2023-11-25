from flask import Flask, render_template

app = Flask(__name__)

TEMPLATES_DIR = "templates/" 

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)