from flask import Flask, render_template, request, jsonify
import jwt
import datetime

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = "123d$!@98w21w1D#D!"  # Change this to a secret key for production

# Simulated user data (replace with your user database logic)
users = {
    'user1': {'password': 'password1', 'role': 'user'},
    'user2': {'password': 'password2', 'role': 'admin'}
}

# Render login page
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print("data " + str(data))
    username = data.get('username')
    password = data.get('password')

    credentials = users.get(username)
    if credentials and password == credentials['password']:
        print("username" + str(username))
        print("password" + str(password))
        payload = {
            'username': str(username),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Token expiration time
        }
        token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
        print("token " + str(token))
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/')
def index():
    return render_template("index.html")

# Protected route example - Requires a valid JWT token to access
# @app.route('/appointments', methods=['GET'])
# def appointments():
#     token = request.headers.get('Authorization')
#     if not token:
#         return jsonify({'message': 'Missing token'}), 401

#     try:
#         decoded = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
#         return jsonify({'username': decoded['username']}), 200
#     except jwt.ExpiredSignatureError:
#         return jsonify({'message': 'Token expired'}), 401
#     except jwt.InvalidTokenError:
#         return jsonify({'message': 'Invalid token'}), 401

@app.route("/appointments")
def appointments():
    return render_template('appointments.html')

@app.route('/doctors')
def doctors():
    doctor_data = [
        {'id': 1, 'name': 'Dr. Smith', 'specialty': 'Cardiologist'},
        {'id': 2, 'name': 'Dr. Johnson', 'specialty': 'Dermatologist'},
    ]

    # TODO Replace with call from Database
    return jsonify(doctor_data), 200

if __name__ == '__main__':
    app.run(debug=True)