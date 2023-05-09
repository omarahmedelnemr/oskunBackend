from flask import Flask, request, jsonify, make_response
import jwt
import mysql.connector
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__)
CORS(app)

# MySQL configuration
myDB = mysql.connector.connect(
    host = 'mysql-124748-0.cloudclusters.net',
    port = 18166,
    user = 'admin',
    password = 'wXA5BMti',
    database = 'oskun'    
)

mycursor = myDB.cursor()

# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    cursor = myDB.cursor()

    # Check if the user exists in the Users table
    query = f"SELECT * FROM User WHERE email = '{email}' AND password = '{password}'"
    print(query)
    cursor.execute(query)
    user = cursor.fetchone()
    cursor.close()
    print(user)
    # Close the database connection
    if user:
        print("INside ")
        # Generate JWT token
        payload = {
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'phoneNumber':user[4],
            'imgDir':user[6]
        }
        token = jwt.encode(payload, 'oskun', algorithm='HS256')

        # Set JWT as a cookie in the response
        response = make_response(jsonify({'massege': 'Done',"token":token}))
        response.set_cookie('token', token)

        return response, 200
    else:
        return jsonify({'massege': 'Somthing went Wrong'}), 200




# Endpoint for user signup
@app.route('/register', methods=['POST'])
def signup():
    try:
        email = request.json.get('email')
        name = request.json.get('name')
        phonenumber = request.json.get('phonenumber')
        password = request.json.get('password')
        imgDir = 'https;//None.png'

        # Connect to the MySQL database
        cursor = myDB.cursor()

        # check if User Exist 
        query = f"SELECT * FROM User WHERE email = '{email}'"
        cursor.execute(query)
        if cursor.fetchall() !=[]:
             return {"massege":"Email Are Already in Use"}
        


        # Insert a new user into the Users table
        query = f"INSERT INTO User VALUES (default, '{name}', '{email}', '{password}', '{phonenumber}', 1,'{imgDir}')"
        cursor.execute(query)
        myDB.commit()




        query = f"SELECT * FROM User WHERE email = '{email}'"
        cursor.execute(query)
        newUser = cursor.fetchall()[0]
        # Close the database connection

        cursor.close()
        # Generate JWT token
        payload = {
            'id':newUser[0],
            'name': newUser[1],
            'email': newUser[2],
            'phonenumber': newUser[4],
            'imgDir': newUser[6]
        }
        token = jwt.encode(payload, 'oskun', algorithm='HS256')

        # Return the token in the response
        return jsonify({"massege":"Done",'token': token})
    except:
        return jsonify({'massege': "Somthing went Wrong"})



@app.route('/updatepassword',methods= ['POST'])
def update():
    try:
        email = request.json.get("email")
        password = request.json.get("password")

        cursor = myDB.cursor() 

        # Insert a new user into the Users table
        query = f"UPDATE User SET password = '{password}' WHERE email = '{email}'"
        print(query)
        cursor.execute(query)
        myDB.commit()
        cursor.close()
        return jsonify({"massege":"Done"})
    except:
        return jsonify({'massege': "Somthing went Wrong"})


@app.route('/changePassword',methods= ['POST'])
def change():
    try:
        email = request.json.get("email")
        # oldpassword = request.json.get("oldpassword")
        newpassword = request.json.get("newpassword")

        cursor = myDB.cursor() 
        # Insert a new user into the Users table
        query = f"UPDATE User SET password = '{newpassword}' WHERE email = '{email}'"
        print(query)
        cursor.execute(query)
        myDB.commit()
        cursor.close()
        return jsonify({"massege":"Done"})
    except:
        return jsonify({'massege': "Somthing went Wrong"})

if __name__ == '__main__':
    app.run()
