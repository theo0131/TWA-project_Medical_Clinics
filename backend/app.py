from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import jwt
import datetime
from flask_swagger_ui import get_swaggerui_blueprint
from functools import wraps

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
    'user1': {'password': 'password1', 'role': 'client'},
    'user2': {'password': 'password2', 'role': 'admin'}
}

appointments = [
    {
        'id' : 1,
        'doctor_name' : 'Dr. Smith',
        'date' : '2023-01-01'
    },
    {
        'id' : 2,
        'doctor_name' : 'Dr. Smith',
        'date' : '2023-02-01'
    },
    {
        'id' : 3,
        'doctor_name' : 'Dr. Smith',
        'date' : '2023-02-01'
    },
    {
        'id' : 4,
        'doctor_name' : 'Dr. Smith',
        'date' : '2023-02-01'
    },
    {
        'id' : 5,
        'doctor_name' : 'Dr. Smith',
        'date' : '2023-02-01'
    }
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
    'password': 'postgres',
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
        
#####################################################################################################
def insert_user(firstName, lastName, email, password, type):
    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Insert a new user

        print(firstName)
        cursor.execute("INSERT INTO users (first_name, last_name, email, user_password, user_type) VALUES (%s, %s, %s, %s, %s) RETURNING user_id;", (firstName, lastName, email, password, type))

        print(firstName)
        # Commit the transaction
        connection.commit()

        # Fetch the ID of the inserted user
        user_id = cursor.fetchone()[0]
        print(f"User with ID {user_id} inserted successfully.")

        return user_id

    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor
        if cursor:
            cursor.close()

def get_user_by_email(email):
    try:
        # Create a cursor to perform database operations
        cursor = connection.cursor()

        print(type(email))

        # Execute the SQL query to select the user by username
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        
        print('here2')

        # Fetch the result (if any)
        user = cursor.fetchone()

        if cursor:
            cursor.close()

        if user:
            print(f"User found: {user}")
            return {
                "id": user[0],
                "email": user[3],
                "password": user[4]
            }
        else:
            print("User not found")
            return None

    except (Exception, psycopg2.Error) as error:
        print(f"Error retrieving user: {error}")

    finally:
        # Close the cursor
        if cursor:
            cursor.close()

def get_user_by_id(id):
    try:
        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Execute the SQL query to select the user by username
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (id,))
        
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

def get_pacient_by_user_id(id):
    try:
        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Execute the SQL query to select the user by username
        cursor.execute("SELECT * FROM pacients WHERE user_id = %s", (id,))
        
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

def insert_pacient(user_id, gender, age, medical_history):
    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Insert a new user
        cursor.execute("INSERT INTO pacients (user_id, gender, age, medical_history) VALUES (%s, %s, %s, %s) RETURNING pacient_id", (user_id, gender, age, medical_history))

        # Commit the transaction
        connection.commit()

        # Fetch the ID of the inserted user
        pacient_id = cursor.fetchone()[0]
        print(f"Pacient with ID {pacient_id} inserted successfully.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor
        if cursor:
            cursor.close()

def get_all_doctors():
    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Insert a new user
        cursor.execute("""SELECT medics.medic_id, medics.specialization, users.first_name, users.last_name 
                       FROM medics 
                       JOIN users ON medics.user_id = users.user_id;""")

        # Commit the transaction
        connection.commit()

        # Fetch the ID of the inserted user
        doctors = cursor.fetchall()

        doctors_list = []
        for doctor in doctors:
            doctors_list.append({
                'medic_id': doctor[0],
                'specialization' : doctor[1],
                'firstName' : doctor[2],
                'lastName' : doctor[3]
            })
        print(doctors_list)
        return doctors_list
    
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor
        if cursor:
            cursor.close()

def insert_doctor(user_id, specialization):
    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Insert a new user
        cursor.execute("INSERT INTO medics (user_id, specialization) VALUES (%s, %s) RETURNING medic_id", (user_id, specialization))

        # Commit the transaction
        connection.commit()

        # Fetch the ID of the inserted user
        pacient_id = cursor.fetchone()[0]
        print(f"Pacient with ID {pacient_id} inserted successfully.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor
        if cursor:
            cursor.close()

def get_all_specialties():
    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Insert a new user
        cursor.execute("""SELECT * 
                       FROM specializations;""")

        # Commit the transaction
        connection.commit()

        # Fetch the ID of the inserted user
        specialties = cursor.fetchall()

        specialties_list = []
        for specialty in specialties:
            specialties_list.append({
                'id': specialty[0],
                'name' : specialty[1],
            })
        print(specialties_list)
        return specialties_list
    
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor
        if cursor:
            cursor.close()

###################################################################################################

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers.get("Authorization")
        
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        
        try:
            decoded = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            user = get_user_by_id(decoded["id"])

            if user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401

        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(*args, **kwargs)

    return decorated
##############################################

app = Flask(__name__)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

CORS(app)  # Enable CORS for all routes

app.config['JWT_SECRET_KEY'] = "123d$!@98w21w1D#D!"  # Change this to a secret key for production

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print(data)

    email = data.get('email')
    password = data.get('password')

    print(email)
    credentials = get_user_by_email(email)
    print(credentials)

    if credentials and password == credentials['password']:
        payload = {
            'id': str(credentials['id']),
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
@token_required
def doctors():
    doctors = get_all_doctors()
    return jsonify(doctors), 200

@app.route('/specialties')
def getSpecialties():
    return jsonify(get_all_specialties()), 200

@app.route('/appointments/create', methods=['POST'])
@token_required
def createAppointment():
    data = request.get_json()
    print(data)
    # TODO introdu aceste data in database
    doctors = get_all_doctors()
    return jsonify(doctors), 200

@app.route('/appointments/update', methods=['POST'])
def updateAppointment():
    data = request.get_json()
    print(data)
    # TODO updateaza aceste data in database
    doctors = get_all_doctors()
    return jsonify(doctors), 200

@app.route('/api/appointments/<int:appointment_id>')
@token_required
def view_appointment(appointment_id):
    print("DE AICI")
    appointment = {
        "id" : appointment_id,
        "medic" : "Ion",
        "pacient" : "Vasile",
        "time" : "12:00 PM",
        "reason" : "Ca de ce nu pana la urma",
        "diagnostic" : "Mai stai si tu pe acasa",
        "userType" : "pacient"
    }

    return jsonify(appointment), 200

@app.route('/register', methods=["POST"])
def registerNewUser():
    data = request.get_json()
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    gender = data.get('gender')
    role = data.get('role')
    specialty = data.get('specialty')
    password = data.get('password')
    age = data.get('age')

    print(firstName)

    user_id = insert_user(firstName, lastName, email, password, role)

    if role == "pacient":
        print("INSERTING NEW PACIENT")
        insert_pacient(user_id, gender, age, " ")

    if role == "doctor":
        insert_doctor(user_id, specialty)
    return jsonify({}), 200


if __name__ == '__main__':
    app.run(debug=True)