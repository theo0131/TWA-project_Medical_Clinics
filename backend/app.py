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

import psycopg2

# # Simulated user data (replace with your user database logic)
users = {
    'user1': {'password': 'password1', 'role': 'user'},
    'user2': {'password': 'password2', 'role': 'admin'}
}

doctor_data = [
    {'id': 1, 'name': 'Dr. Smith', 'specialty': 'Cardiologist'},
    {'id': 2, 'name': 'Dr. Johnson', 'specialty': 'Dermatologist'},
]

# steps to connect to postgresql database: install postgresql, 
# start postgresql server: sudo service postgresql start, 
# check with pg_isready, 
# run the sql file: su - postgres
#                   psql -f database.sql
# run app.py

db_params = {
    'host': 'localhost',
    'database': 'medical_network',
    'user': 'postgres',
    'password': 'ola',
    'port': '5432',
}

try:
    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(**db_params)

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Example: Execute a SQL query
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"Connected to the PostgreSQL database. Server version: {version}")

    # You can perform more database operations here...

except (Exception, psycopg2.Error) as error:
    print(f"Error: {error}")

finally:
    if cursor:
        cursor.close()
#     # Close the cursor and connection
#     if connection:
#         cursor.close()
#         connection.close()
#         print("Connection closed.")

##########################################################
def insert_user(username, password, email, type):
    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Insert a new user
        cursor.execute("INSERT INTO users (username, user_password, email, user_type) VALUES (%s, %s, %s, %s) RETURNING user_id", (username, password, email, type))

        # Commit the transaction
        connection.commit()

        # Fetch the ID of the inserted user
        user_id = cursor.fetchone()[0]
        print(f"User with ID {user_id} inserted successfully.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor
        if cursor:
            cursor.close()

def get_user_by_username(username):
    try:
        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Execute the SQL query to select the user by username
        cursor.execute("SELECT * FROM users WHERE username = {}", (username))
        

        # Fetch the result (if any)
        user = cursor.fetchone()

        if user:
            print(f"User found: {user}")
            return user
        else:
            print("User not found")
            return None

    except (Exception, psycopg2.Error) as error:
        print(f"Error retrieving user: {error}")

    finally:
        # Close the cursor
        if cursor:
            cursor.close()

insert_user("user2", "pswd2", "email2@ola.com", "pacient")

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

if __name__ == '__main__':
    app.run(debug=True)