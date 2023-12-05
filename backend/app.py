from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import jwt
import datetime
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
    'host': '172.17.232.145',
    'database': 'medical_network',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432',
}

# try:
#     # Establish a connection to the PostgreSQL database
#     connection = psycopg2.connect(**db_params)

#     # Create a cursor object to interact with the database
#     cursor = connection.cursor()

#     # Example: Execute a SQL query
#     cursor.execute("SELECT version();")
#     version = cursor.fetchone()
#     print(f"Connected to the PostgreSQL database. Server version: {version}")

#     # You can perform more database operations here...

# except (Exception, psycopg2.Error) as error:
#     print(f"Error: {error}")

# finally:
#     if cursor:
#         cursor.close()
#     # Close the cursor and connection
#     if connection:
#         cursor.close()
#         connection.close()
#         print("Connection closed.")

##########################################################
# def insert_user(username, password, email, type):
#     try:
#         # Create a cursor object to interact with the database
#         cursor = connection.cursor()

#         # Insert a new user
#         cursor.execute("INSERT INTO users (username, user_password, email, user_type) VALUES (%s, %s, %s, %s) RETURNING user_id", (username, password, email, type))

#         # Commit the transaction
#         connection.commit()

#         # Fetch the ID of the inserted user
#         user_id = cursor.fetchone()[0]
#         print(f"User with ID {user_id} inserted successfully.")

    # except (Exception, psycopg2.Error) as error:
    #     print(f"Error: {error}")

    # finally:
    #     # Close the cursor
    #     if cursor:
    #         cursor.close()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['JWT_SECRET_KEY'] = "123d$!@98w21w1D#D!"  # Change this to a secret key for production

@app.route("/login", methods=["POST"])
def login():
    print("inceput")
    data = request.get_json()
    print(data)
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

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')

    # insert_user(username, password, email, role)
    return jsonify({'message': 'User Registered'}), 200