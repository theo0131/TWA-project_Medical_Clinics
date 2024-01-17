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
        
#############################################  users ops ########################################################
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

        # Execute the SQL query to select the user by username
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        
        # Fetch the result (if any)
        user = cursor.fetchone()

        if cursor:
            cursor.close()

        if user:
            # print(f"User found: {user}")
            return {
                "id": user[0],
                "email": user[3],
                "password": user[4],
                "type": user[5]
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
            # print(f"User found: {user}")
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
            # print(f"User found: {user}")
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
        cursor.execute("""SELECT medics.medic_id, medics.specialization, users.first_name, users.last_name, users.user_id
                       FROM medics 
                       JOIN users ON medics.user_id = users.user_id;""")

        # Commit the transaction
        connection.commit()

        # Fetch the ID of the inserted user
        doctors = cursor.fetchall()

        doctors_list = []
        for doctor in doctors:
            doctors_list.append({
                'doctor_id': doctor[0],
                'specialization' : doctor[1],
                'name' : str(doctor[2]) + " " + str(doctor[3]),
                'user_id' : doctor[4]
            })
        return doctors_list
    
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor
        if cursor:
            cursor.close()

def get_all_pacients():
    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Insert a new user
        cursor.execute("""SELECT pacients.pacient_id, pacients.gender, pacients.age, users.first_name, users.last_name, users.user_id 
                       FROM pacients 
                       JOIN users ON pacients.user_id = users.user_id;""")

        # Commit the transaction
        connection.commit()

        # Fetch the ID of the inserted user
        pacients = cursor.fetchall()

        pacients_list = []
        for pacient in pacients:
            pacients_list.append({
                'pacient_id': pacient[0],
                'gender' : pacient[1],
                'age' : pacient[2],
                'name' : str(pacient[3]) + " " + str(pacient[4]),
                'user_id' : pacient[5]
            })
        return pacients_list
    
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

#############################################  locations ops ########################################################

def insert_locations(address_name):
    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO locations 
            (address_name) 
            VALUES (%s)
        """, (address_name,))

        # Commit the transaction
        connection.commit()

        print("Location inserted successfully!")

    except psycopg2.Error as e:
        print("Error inserting location:", e)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()

def get_all_locations():
    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Insert a new user
        cursor.execute("""SELECT * 
                       FROM locations;""")

        # Commit the transaction
        connection.commit()

        # Fetch the ID of the inserted user
        locations = cursor.fetchall()

        locations_list = []
        for location in locations:
            locations_list.append({
                'id': location[0],
                'name' : location[1],
            })
        return locations_list
    
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor
        if cursor:
            cursor.close()

#############################################  appointements ops ########################################################

def insert_appointment(pacient_id, medic_id, reason, timestamp):
    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO appointments 
            (pacient_id, medic_id, reason, appmt_timestamp) 
            VALUES (%s, %s, %s, %s)
        """, (pacient_id, medic_id, reason, timestamp))

        # Commit the transaction
        connection.commit()

        print("Appointment inserted successfully!")

    except psycopg2.Error as e:
        print("Error inserting appointment:", e)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        # if connection:
        #     connection.close()

def remove_appointment(connection_params, appmt_id):
    try:
       
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM appointments WHERE appmt_id = %s
        """, (appmt_id))

        # Commit the transaction
        connection.commit()

        print(f"Appointment with ID {appmt_id} removed successfully!")

    except psycopg2.Error as e:
        print("Error removing appointment:", e)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()

def add_diagnostic(appmt_id, diagnostic):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE appointments SET diagnostic = %s WHERE appmt_id = %s
        """, (diagnostic, appmt_id))

        # Commit the transaction
        connection.commit()

        print(f"Diagnostic for appointment with ID {appmt_id} modified successfully!")

    except psycopg2.Error as e:
        print("Error modifying diagnostic:", e)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()

def get_appointment_details(appmt_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
           SELECT * FROM appointments WHERE appmt_id = %s
        """, (appmt_id))

        # Fetch the result
        result = cursor.fetchone()

        if result:
            # Convert the result to a dictionary for easy access
            columns = [desc[0] for desc in cursor.description]
            appointment_details = dict(zip(columns, result))
            return appointment_details
        else:
            print(f"Appointment with ID {appmt_id} not found.")
            return None

    except psycopg2.Error as e:
        print("Error retrieving appointment details:", e)
        return None

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()

def get_all_appointments():
    try:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM appointments;""")

        # Commit the transaction
        connection.commit()

        # Fetch the ID of the inserted user
        appointments = cursor.fetchall()
        pacient_list = {}
        for pacient in get_all_pacients():
            pacient_list[pacient['pacient_id']] = pacient
        pacient_id_mapping = {}
        for pacient in pacient_list.values():
            pacient_id_mapping[pacient['pacient_id']] = pacient['user_id']

        doctors_list = {}
        for doctor in get_all_doctors():
            doctors_list[doctor['doctor_id']] = doctor
        doctors_id_mapping = {}
        for doctors in doctors_list.values():
            doctors_id_mapping[doctors['doctor_id']] = doctors['user_id']

        locations_list = {}
        for location in get_all_locations():
            locations_list[location['id']] = location


        appointments_list = []
        for appointment in appointments:
            appointments_list.append({
                'id': appointment[0],
                'pacient_id' : pacient_id_mapping[pacient_list[appointment[1]]['pacient_id']],
                'pacient' : pacient_list[appointment[1]]['name'],
                'doctor_id' : doctors_id_mapping[doctors_list[appointment[2]]['doctor_id']],
                'doctor' : doctors_list[appointment[2]]['name'],
                # 'address' : locations_list[appointment[5]]['name'],
                'time': appointment[6],
                'reason' : appointment[7],
                'diagnostic' : appointment[8]
            })
        return appointments_list
    
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor
        if cursor:
            cursor.close()

def delete_appointment_db(id):
    try:
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM appointments WHERE appmt_id=%s;""", (str(id)))

        # Commit the transaction
        connection.commit()

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

currentUserType = None
loggedUserId = None

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

    global currentUserType
    currentUserType = credentials['type']

    if credentials and password == credentials['password']:
        global loggedUserId
        loggedUserId = credentials['id']
        payload = {
            'id': str(credentials['id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Token expiration time
        }
        token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/doctors')
@token_required
def doctors():
    return jsonify(get_all_doctors()), 200

@app.route('/pacients')
@token_required
def pacients():
    return jsonify(get_all_pacients()), 200

@app.route('/specialties')
def getSpecialties():
    return jsonify(get_all_specialties()), 200

@app.route('/appointments')
@token_required
def getAppointments():
    global currentUserType, loggedUserId
    if currentUserType == "pacient":
        appointments = [app for app in get_all_appointments() if app['pacient_id'] == loggedUserId]
    else:
        appointments = [app for app in get_all_appointments() if app['doctor_id'] == loggedUserId]

    return jsonify({
            "appointments": appointments,
            "userType": currentUserType
        }), 200

@app.route('/appointments/create', methods=['POST'])
@token_required
def createAppointment():
    data = request.get_json()
    pacient_list = {}
    for pacient in get_all_pacients():
        pacient_list[pacient['pacient_id']] = pacient
    pacient_id_mapping = {}
    for pacient in pacient_list.values():
        pacient_id_mapping[pacient['user_id']] = pacient['pacient_id']

    global loggedUserId
    insert_appointment(pacient_id_mapping[loggedUserId], data['doctor_id'], data['reason'], data['appointmentDate'])
    return jsonify({}), 200

@app.route('/appointments/update', methods=['POST'])
@token_required
def updateAppointment():
    data = request.get_json()
    add_diagnostic(data['id'], data['diagnostic'])
    return jsonify({}), 200

@app.route('/api/appointments/<int:appointment_id>')
@token_required
def view_appointment(appointment_id):
    global currentUserType
    all_appointments = get_all_appointments()
    for appointment in all_appointments:
        if appointment['id'] == appointment_id:
            return jsonify({
                "appointment": appointment,
                "userType" : str(currentUserType)
            }), 200

@app.route('/api/appointments/delete/<int:appointment_id>', methods=['DELETE'])
@token_required
def delete_appointment(appointment_id):
    print('Delete appointment', appointment_id)
    delete_appointment_db(appointment_id)
    return jsonify({}), 200

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