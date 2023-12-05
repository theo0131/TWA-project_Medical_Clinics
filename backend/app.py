# from flask import Flask, render_template, request, jsonify
# import jwt
# import datetime

# app = Flask(__name__)

# # Simulated user data (replace with your user database logic)
# users = {
#     'user1': {'password': 'password1', 'role': 'user'},
#     'user2': {'password': 'password2', 'role': 'admin'}
# }

# @app.route('/', methods=['GET'])
# def show_users():
#     return jsonify(users), 200

# @app.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     print("data " + str(data))
#     username = data.get('username')
#     password = data.get('password')

#     credentials = users.get(username)
#     if credentials and password == credentials['password']:
#         print("username" + str(username))
#         print("password" + str(password))
#         payload = {
#             'username': str(username),
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Token expiration time
#         }
#         token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
#         print("token " + str(token))
#         return jsonify({'token': token}), 200
#     else:
#         return jsonify({'message': 'Invalid credentials'}), 401

# # Protected route example - Requires a valid JWT token to access
# # @app.route('/appointments', methods=['GET'])
# # def appointments():
# #     token = request.headers.get('Authorization')
# #     if not token:
# #         return jsonify({'message': 'Missing token'}), 401

# #     try:
# #         decoded = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
# #         return jsonify({'username': decoded['username']}), 200
# #     except jwt.ExpiredSignatureError:
# #         return jsonify({'message': 'Token expired'}), 401
# #     except jwt.InvalidTokenError:
# #         return jsonify({'message': 'Invalid token'}), 401

# @app.route('/doctors')
# def doctors():
#     doctor_data = [
#         {'id': 1, 'name': 'Dr. Smith', 'specialty': 'Cardiologist'},
#         {'id': 2, 'name': 'Dr. Johnson', 'specialty': 'Dermatologist'},
#     ]

#     # TODO Replace with call from Database
#     return jsonify(doctor_data), 200

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import jwt
import datetime
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API',
        'displayOperationId': True,
        'displayRequestDuration': True,
        'supportedSubmitMethods': ['get', 'post', 'put', 'delete'],
    },
)

# # Simulated user data (replace with your user database logic)
users = {
    'user1': {'password': 'password1', 'role': 'user'},
    'user2': {'password': 'password2', 'role': 'admin'}
}

doctor_data = [
    {'id': 1, 'name': 'Dr. Smith', 'specialty': 'Cardiologist'},
    {'id': 2, 'name': 'Dr. Johnson', 'specialty': 'Dermatologist'},
]

app = Flask(__name__)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

CORS(app)  # Enable CORS for all routes

app.config['JWT_SECRET_KEY'] = "123d$!@98w21w1D#D!"  # Change this to a secret key for production

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    credentials = users.get(username)
    if credentials and password == credentials['password']:
        payload = {
            'username': str(username),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Token expiration time
        }
        token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/users')
def get_users():
    users = [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Jane"},
        # Add more users as needed
    ]
    return jsonify(users)

@app.route('/doctors')
def doctors():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        decoded = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return jsonify(doctor_data), 200
    except jwt.ExpiredSignatureError:
        print("ExpiredSignatureError")
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        print("InvalidTokenError")
        return jsonify({'message': 'Invalid token'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')

    # insert_user(username, password, email, role)
    return jsonify({'message': 'User Registered'}), 200

if __name__ == '__main__':
    app.run(debug=True)