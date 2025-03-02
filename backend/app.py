from flask_mysqldb import MySQL
from flask import Flask, request, jsonify  


app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = 'root'  
app.config['MYSQL_DB'] = 'blood_donation'

mysql = MySQL(app)

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email & password are required"}), 400

    try:
        cursor = mysql.connection.cursor()
        
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            return jsonify({"error": "User already exists"}), 400

      
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "User registration successful"}), 201

    except Exception as e:
        print(f"Error during signup: {e}") 
        return jsonify({"error": "An error occurred during registration"}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        cursor = mysql.connection.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if not user:
            return jsonify({"error": "Invalid email or password"}), 401


        if user[2] != password:  
            return jsonify({"error": "Invalid email or password"}), 401

      
        return jsonify({"message": "Login successful"}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred during login"}), 500

if __name__ == '_main_':
    app.run(debug=True)