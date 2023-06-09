from flask import Flask, request, jsonify, make_response,render_template_string
import jwt
import mysql.connector
from flask_cors import CORS
import datetime


app = Flask(__name__)
CORS(app)

# MySQL configuration
myDB = mysql.connector.connect(
    host = 'mysql-126454-0.cloudclusters.net',
    port = 10008,
    user = 'admin',
    password = 'dUWDxqxb',
    database = 'oskun'    
)



def addLabels(data,legends, nasted):
    singleDict = {}
    result = []
    if nasted:
        for i in data:
                for x  in range(len(i)):
                    singleDict[legends[x][0]] = i[x]
                result.append(singleDict)
                singleDict = {}
        return result
    else:
        for x  in range(len(data)):
            singleDict[legends[x][0]] = data[x]
        return singleDict


@app.route('/')
def Home():
   return  render_template_string('<h1 style="text-align:center">This is Our Server Running</h1>')

# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    cursor = myDB.cursor()

    try: 

        email = request.json.get('email')
        password = request.json.get('password')

        

        # Check if the user exists in the Users table
        query = f"SELECT * FROM User WHERE email = '{email}' AND password = '{password}'"
        print(f"Query ;{query}")
        cursor.execute(query)
        user = cursor.fetchall()
        
        print(user)
        # Close the database connection
        if len(user)!=0:
            user=user[0]
            # Generate JWT token
            payload = {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'phoneNumber':user[4],
                'imgDir':user[6]
            }
            token = jwt.encode(payload, 'oskun', algorithm='HS256')

            response =  jsonify({'message': 'Done',"token":token})
        else:
            
            response =  jsonify({'message': 'Somthing went Wrong'})
    except:
            
            response = jsonify({'message': 'Somthing went Wrong'})

    cursor.close()
    print(response)
    return response

# Endpoint for user signup
@app.route('/register', methods=['POST'])
def signup():
    cursor = myDB.cursor()
    try: 

        email = request.json.get('email')
        name = request.json.get('name')
        phonenumber = request.json.get('phonenumber')
        password = request.json.get('password')
        imgDir = 'https://i.pinimg.com/736x/8b/16/7a/8b167af653c2399dd93b952a48740620.jpg'

        # Connect to the MySQL database
        

        # check if User Exist 
        query = f"SELECT * FROM User WHERE email = '{email}'"
        cursor.execute(query)
        if cursor.fetchall() !=[]:
             cursor.close()
             return {"message":"Email Are Already in Use"}
        


        # Insert a new user into the Users table
        query = f"INSERT INTO User VALUES (default, '{name}', '{email}', '{password}', '{phonenumber}', 1,'{imgDir}')"
        cursor.execute(query)
        myDB.commit()




        query = f"SELECT * FROM User WHERE email = '{email}'"
        cursor.execute(query)
        newUser = cursor.fetchall()[0]
        # Close the database connection

        
        # Generate JWT token
        payload = {
            'id':newUser[0],
            'name': newUser[1],
            'email': newUser[2],
            'phoneNumber': newUser[4],
            'imgDir': newUser[6]
        }
        token = jwt.encode(payload, 'oskun', algorithm='HS256')

        # Return the token in the response
        response =  jsonify({"message":"Done",'token': token})
    except:
        response =  jsonify({'message': "Somthing went Wrong"})


    cursor.close()
    print(response)
    return response

@app.route('/updatepassword',methods= ['POST'])
def update():
    cursor = myDB.cursor()
    try:

        email = request.json.get("email")
        password = request.json.get("newPassword")

        # Insert a new user into the Users table
        query = f"UPDATE User SET password = '{password}' WHERE email = '{email}'"
        print(query)
        cursor.execute(query)
        myDB.commit()
        
        response =  jsonify({"message":"Done"})
    except:
        response =  jsonify({'message': "Somthing went Wrong"})

    cursor.close()
    print(response)
    return response


@app.route('/changePassword',methods= ['POST'])
def change():
    try:
        cursor = myDB.cursor()

        email = request.json.get("email")
        # oldpassword = request.json.get("oldpassword")
        newpassword = request.json.get("newPassword")

         
        # Insert a new user into the Users table
        query = f"UPDATE User SET password = '{newpassword}' WHERE email = '{email}'"
        print(query)
        cursor.execute(query)
        myDB.commit()
        
        cursor.close()
        return jsonify({"message":"Done"})
    except:
        return jsonify({'message': "Somthing went Wrong"})



# Nady Part

@app.route("/profile" )
def index():

    arb = request.args
    id = arb.get('id') 
    if id ==None:
        return {"message":"Somthing went Wrong"}
    else:
        try:
            cursor = myDB.cursor()

            cursor.execute(f"SELECT * FROM User WHERE id = {id}" )
            usr = cursor.fetchone()

            # myDB.commit() 
            usr = addLabels(usr,cursor.description,0)

            cursor.close()
            return {"message":"Done","data":usr}
        except:
            return {"message":"Somthing went Wrong"}

@app.route("/favorite")
def getfv():
    f = request.args
    id =f.get('id') 
    if id ==None:
        return {"message":"Somthing went Wrong"}
    else:
        cursor = myDB.cursor()

        cursor.execute(f"SELECT * FROM Favorite WHERE userID = {id} " )
        fav = cursor.fetchall()
        fav = addLabels(fav,cursor.description,1)


        houseFavorite = []
        for i in fav:
            cursor.execute(f"SELECT * FROM House WHERE id = {i['HouseID']}")
            house = cursor.fetchone()
            house = addLabels(house,cursor.description,0)
            houseFavorite.append(house) 
        cursor.close()
        return {"message":"Done","data":houseFavorite}

@app.route('/updateuser', methods=['POST'])
def update_user():

    try:
        cursor = myDB.cursor()

        idd = request.json.get('id')
        name = request.json.get('name')
        email = request.json.get('email')
        phone_number = request.json.get('phoneNumber')


        sql = f"UPDATE User SET name = '{name}', email = '{email}' ,phoneNumber = '{phone_number}' WHERE id = {idd}"
        print(sql)
        cursor.execute(sql)
        myDB.commit()
        
        cursor.close()
        return {"message":"Done"}
    except:
        return {"message":"Somthing went Wrong"}

@app.route("/history")
def hist():
    arb = request.args
    id = arb.get('id')
    if id ==None:
        return {"message":"Somthing went Wrong"}
    else:
        try:
            cursor = myDB.cursor()

            cursor.execute(f"SELECT * FROM History WHERE userID =  {id}" )
            his = cursor.fetchall()

            his = addLabels(his,cursor.description,1)
            houseHistory = []
            for i in his:
                cursor.execute(f"SELECT * FROM House WHERE id = {i['house']}")
                house = cursor.fetchone()
                house = addLabels(house,cursor.description,0)
                house['history'] = i
                houseHistory.append(house) 

            cursor.close()
            return {"message":"Done","data":houseHistory}
        except:
            return {"message":"Somthing went Wrong"}

@app.route('/addhouse', methods=['POST'])
def add_property():
    try:
        cursor = myDB.cursor()
        
        owner = request.json.get('owner')
        name = request.json.get('name')
        location = request.json.get('location')
        description = request.json.get('description')
        mainImg = request.json.get('mainImg')

        images = request.json.get('images')

        rooms = request.json.get('rooms')
        beds = request.json.get('beds')
        baths = request.json.get('baths')
        size = request.json.get('size')
        price = request.json.get('price')

        cash = request.json.get('cash')
        typ = request.json.get('type')
        dayRent = request.json.get('dayRent')
        weekRent = request.json.get('weekRent')        
        
        publishDate = datetime.datetime.now()
        rating = 2.5 #as it is Not Rated Yet #request.json.get('rating')
        avilable = 1
        
        sql = f"INSERT INTO House (owner, type, name, location, publishDate, rating, rooms, beds, size, price, mainImg, avilable, cash, dayRent, weekRent, description,baths) VALUES ({owner}, '{typ}', '{name}', '{location}', '{publishDate}', {rating}, {rooms}, {beds}, {size}, {price}, '{mainImg}', {avilable}, {cash}, {dayRent}, {weekRent}, '{description}',{baths})"
        cursor.execute(sql)
        myDB.commit()

        houseID = cursor.lastrowid
        print("Before")
        cursor.execute(f"INSERT INTO images VALUES (default,{houseID},'{images[0]['imageDirectory']}')")
        cursor.execute(f"INSERT INTO images VALUES (default,{houseID},'{images[1]['imageDirectory']}')")
        print("After")
        myDB.commit()

        cursor.close()
        # for i in images:
        #     imageQuery+=f"INSERT INTO images VALUES (defualt,{houseID},'{i}');"
        # print(imageQuery)
        # cursor.execute(imageQuery)
        # myDB.commit()
        return {"message":"Done"}
    except:
        return {"message":"Somthing went Wrong"}



@app.route('/edithouse', methods=['POST'])
def edit_property():
    try:
        cursor = myDB.cursor()
        
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
        cursor.close()
        
        return {"message":"Done"}
    except:
        return {"message":"Somthing went Wrong"}
        


@app.route('/deletehouse', methods=['Delete'])
def delete_property():
    
    idd = request.json.get('id')
    if idd == None:
        return {"message":"Somthing went Wrong"}
    else:
        cursor = myDB.cursor()

        sql = f"DELETE FROM Favorite WHERE HouseID = {idd}"
        cursor.execute(sql)
        
        sql = f"DELETE FROM House WHERE id = {idd}"
        cursor.execute(sql)
        myDB.commit()
        
        cursor.close()
        return {"message":"Done"}






@app.route('/ratehouse', methods=['POST'])
def rate_property():

    idd = request.json.get('id')
    rating = request.json.get('rating')
    if idd ==None or rating == None:
        return {"message":"Somthing went Wrong"}
    else:
        cursor = myDB.cursor()
        
        sql = f"UPDATE House SET rating = {rating} WHERE id = {idd}"
        cursor.execute(sql)
        myDB.commit()
        
        cursor.close()
        return {"message":"Done"}




@app.route('/checkout', methods=['POST'])
def rentingdetails():
    try:
    
        cursor = myDB.cursor()
        
        idd = request.json.get('HouseID')
        if idd ==None:
           return {"message":"Somthing went Wrong"}

        sql = f"UPDATE House SET avilable = 1 WHERE id = {idd}"
        cursor.execute(sql)
        
        cursor.execute(f"SELECT * FROM RentingActivity WHERE HouseID = {idd} " )
        ren = cursor.fetchone()
        
        sql = f"INSERT INTO History (house, userID, startDate, endDate, rentingPrice) VALUES ({ren[1]}, {ren[2]}, '{ren[3]}', '{ren[4]}', {ren[5]})"
        cursor.execute(sql)

        sql = f"DELETE FROM RentingActivity WHERE id = {idd}"
        cursor.execute(sql)
        
        myDB.commit()
        cursor.close()
        return {"message":"Done"}
    except:
        return {"message":"Somthing went Wrong"}





# Kareem Part


#when we get to this endpoint
@app.route("/latestten")   
def get_latest_ten():
    try:
    
        cursor = myDB.cursor()
        
        query = "SELECT * FROM House WHERE avilable = 1 ORDER BY publishDate DESC LIMIT 10"
        cursor.execute(query)
        result = cursor.fetchall()
        
        result = addLabels(result,cursor.description,1)

        cursor.close()
        return {"message":"Done","data":result}
    except:
        return {"message":"Somthing went Wrong"}


@app.route("/AvailableHouses")
def Get_Availabe():

    try:
        cursor = myDB.cursor()
        query = "SELECT * FROM House WHERE avilable = 1 " #sql code to get the most recent 10 houses 
        cursor.execute(query)
        result = cursor.fetchall()

        result = addLabels(result,cursor.description,1)        
        cursor.close()
        return {"message":"Done","data":result}
    except:
        return {"message":"Somthing went Wrong"}

@app.route("/HouseDetails")
def view_details():
    try:
        id = request.args.get("id")
        if id ==None:
            return {"message":"Somthing went Wrong"}
        
        cursor = myDB.cursor()

        #get House Details
        query = f"SELECT * FROM House WHERE id = {id}" #sql code to get the most recent 10 houses 
        print(query)
        cursor.execute(query)
        houseInfo = cursor.fetchone()

        #Add The Columns Names
        houseInfoResult=addLabels(houseInfo,cursor.description,0)

        #Get the images Related To That House 
        query = f"SELECT * FROM images WHERE HouseID = {id}" #sql code to get the most recent 10 houses 
        print(query)
        cursor.execute(query)
        images = cursor.fetchall()

        #Add The Columns Names
        imagesInfo = addLabels(images,cursor.description,1)

        #Put Images in All Data
        houseInfoResult['images'] = imagesInfo

        cursor.close()
        return {"message":"Done","data":houseInfoResult}
    except:
        return {"message":"Somthing went Wrong"}
    

@app.route("/booking", methods=["POST"])
def renter_booking():
    try:

        # Parse request body for booking details
        data = request.json
        user_id = data["userId"]
        House_id = data["HouseId"]
        start_date = data["startDate"]
        end_date = data["endDate"]
        price = data["price"]
        willRenew = data["willRenew"]

        
        # Insert booking details into database
        cursor = myDB.cursor()
        query = f"INSERT INTO RentingActivity VALUES (default , {House_id}, {user_id}, '{start_date}', '{end_date}', {price},{willRenew})"
        cursor.execute(query)


        query = f"UPDATE House SET avilable=0 WHERE id={House_id}"
        cursor.execute(query)

        myDB.commit()
        # Return success response
        cursor.close()
        return {"message":"Done"}
        

    except:
        return {"message":"Somthing went Wrong"}


@app.route('/unbooking', methods=['POST'])
def unbooking():
    try:

        print("Hello")
        # Extract data from JSON payload
        data = request.json
        userID = data['userId']
        HouseID = data['HouseId']
        print(f"Hello {userID}, {HouseID}")

        # Connect to database and execute query
        cursor = myDB.cursor()
        query = f"DELETE FROM RentingActivity WHERE userID = {userID} AND HouseID = {HouseID}"
        cursor.execute(query)
        myDB.commit()
        

        # Return success message
        cursor.close()
        return {"message":"Done"}
    except:
        return {"message":"Somthing went Wrong"}



@app.route("/extendbooking", methods=["POST"])
def extend_booking():
    try:

        cursor = myDB.cursor()
        # Get data from request JSON
        data = request.json
        booking_id = data["bookingID"]
        extensionDate = data["extensionDays"]

        # Get current checkout date and calculate new checkout date
        query = f"SELECT * FROM RentingActivity WHERE id = {booking_id}"
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)
        if result ==None:
            return {"message":"Somthing went Wrong"}
        
        # Update checkout date in database
        query = f"UPDATE RentingActivity SET endDate = '{extensionDate}' WHERE id = {booking_id}"
        print(query)
        cursor.execute(query)
        myDB.commit()

        cursor.close()
        return {"message":"Done"}
    except:
        return {"message":"Somthing went Wrong"}
    


if __name__ == '__main__':
    app.run(debug=True,port=5000)
