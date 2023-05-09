from flask import Flask, request, jsonify, make_response,render_template_string
import jwt
import mysql.connector
from flask_cors import CORS
import datetime


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

cursor = myDB.cursor()

@app.route('/')
def Home():
   return  render_template_string('<h1 style="text-align:center">This is Our Server Running</h1>')

# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    

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

         
        # Insert a new user into the Users table
        query = f"UPDATE User SET password = '{newpassword}' WHERE email = '{email}'"
        print(query)
        cursor.execute(query)
        myDB.commit()
        cursor.close()
        return jsonify({"massege":"Done"})
    except:
        return jsonify({'massege': "Somthing went Wrong"})


# Nady Part

@app.route("/profile" )
def index():

    arb = request.args
    id = arb.get('id') 
    if id ==None:
        return {"massege":"Wrong"}
    else:
        try:

            cursor.execute(f"SELECT * FROM User WHERE id = {id}" )
            usr = cursor.fetchall()

            myDB.commit() 
            return {"massege":"Done","data":usr}
        except:
            return {"massege":"Wrong"}

@app.route("/favorite")
def getfv():
    f = request.args
    id =f.get('id') 
    if id ==None:
        return {"massege":"Wrong"}
    else:
        cursor.execute(f"SELECT * FROM Favorite WHERE id = {id} " )
        fav = cursor.fetchone()
        myDB.commit()
        return {"massege":"Done","data":fav}

@app.route('/updateuser', methods=['POST'])
def update_user():

    try:

        idd = request.json.get('id')
        name = request.json.get('name')
        email = request.json.get('email')
        password = request.json.get('password')
        phone_number = request.json.get('phoneNumber')
        showNumber = request.json.get('showNumber')
        img_dir = request.args.get('imgDir')


        sql = f"UPDATE User SET name = '{name}', email = '{email}', password = '{password}',imgDir = '{img_dir}' ,phoneNumber = '{phone_number}', showNumber = {showNumber} WHERE id = {idd}"
        cursor.execute(sql)
        myDB.commit()
        
        return {"massege":"Done"}
    except:
        return {"massege":"Wrong"}

@app.route("/history" , methods = ['POST', 'GET'])
def hist():
    arb = request.args
    id = arb.get('id')
    if id ==None:
        return {"massege":"Wrong"}
    else:
        cursor.execute(f"SELECT * FROM History WHERE id =  {id}" )
        his = cursor.fetchall()
        myDB.commit() 
        return {"massege":"Done","data":his}

@app.route('/addhouse', methods=['POST'])
def add_property():
    try:
        owner = request.json.get('owner')
        typ = request.json.get('type')
        name = request.json.get('name')
        location = request.json.get('location')
        publishDate = datetime.datetime.now()
        rating = request.json.get('rating')
        rooms = request.json.get('rooms')
        beds = request.json.get('beds')
        baths = request.json.get('baths')

        size = request.json.get('size')
        price = request.json.get('price') 
        mainImg = request.json.get('mainImg')
        avilable = request.json.get('avilable')
        cash = request.json.get('cash')
        dayRent = request.json.get('dayRent')
        weekRent = request.json.get('weekRent')
        description = request.json.get('description')
        
        sql = f"INSERT INTO House (owner, type, name, location, publishDate, rating, rooms, beds, size, price, mainImg, avilable, cash, dayRent, weekRent, description,baths) VALUES ({owner}, '{typ}', '{name}', '{location}', {publishDate}, {rating}, {rooms}, {beds}, {size}, {price}, '{mainImg}', {avilable}, {cash}, {dayRent}, {weekRent}, '{description}',{baths})"
        cursor.execute(sql)
        myDB.commit()
        
        return {"massege":"Done"}
    except:
        return {"massege":"Wrong"}



@app.route('/edithouse', methods=['POST'])
def edit_property():
    try:
        idd = request.json.get('id')
        owner = request.json.get('owner')
        typ = request.json.get('type')
        name = request.json.get('name')
        location = request.json.get('location')
        publishDate = request.json.get('publishDate')
        rating = request.json.get('rating')
        rooms = request.json.get('rooms')
        beds = request.json.get('beds')
        baths = request.json.get('baths')

        size = request.json.get('size')
        price = request.json.get('price') 
        mainImg = request.json.get('mainImg')
        avilable = request.json.get('avilable')
        cash = request.json.get('cash')
        dayRent = request.json.get('dayRent')
        weekRent = request.json.get('weekRent')
        description = request.json.get('description')
        
        sql = f"UPDATE House SET owner = {owner}, type = '{typ}', name = '{name}', location = '{location}', publishDate = '{publishDate}', rating = {rating}, rooms = {rooms}, beds = {beds}, size = {size}, price = {price}, mainImg = '{mainImg}', avilable = {avilable}, cash = {cash}, dayRent = {dayRent}, weekRent = {weekRent}, description = '{description}', baths = {baths} WHERE id = {idd}"
        cursor.execute(sql)
        myDB.commit()
        
        return {"massege":"Done"}
    except:
        return {"massege":"Wrong"}
        


@app.route('/deletehouse', methods=['Delete'])
def delete_property():
    
    idd = request.json.get('id')
    if idd == None:
        return {"massege":"Wrong"}
    else:

        sql = f"DELETE FROM Favorite WHERE HouseID = {idd}"
        cursor.execute(sql)
        
        sql = f"DELETE FROM House WHERE id = {idd}"
        cursor.execute(sql)
        myDB.commit()
        
        return {"massege":"Done"}






@app.route('/ratehouse', methods=['POST'])
def rate_property():

    idd = request.json.get('id')
    rating = request.json.get('rating')
    if idd ==None or rating == None:
        return {"massege":"Wrong"}
    else:
        sql = f"UPDATE House SET rating = {rating} WHERE id = {idd}"
        cursor.execute(sql)
        myDB.commit()
        
        return {"massege":"Done"}




@app.route('/checkout', methods=['POST'])
def rentingdetails():
    try:
    
        idd = request.json.get('HouseID')
        if idd ==None:
           return {"massege":"Wrong"}

        sql = f"UPDATE House SET avilable = 1 WHERE id = {idd}"
        cursor.execute(sql)
        
        cursor.execute(f"SELECT * FROM RentingActivity WHERE HouseID = {idd} " )
        ren = cursor.fetchone()
        
        sql = f"INSERT INTO History (house, userID, startDate, endDate, rentingPrice) VALUES ({ren[1]}, {ren[2]}, '{ren[3]}', '{ren[4]}', {ren[5]})"
        cursor.execute(sql)

        sql = f"DELETE FROM RentingActivity WHERE id = {idd}"
        cursor.execute(sql)
        
        myDB.commit()
        return {"massege":"Done"}
    except:
        return {"massege":"Wrong"}








if __name__ == '__main__':
    app.run(debug=True,port=8000)
