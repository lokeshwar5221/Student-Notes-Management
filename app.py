from config import Config
import mysql.connector as sql
import random 
DBConfig = Config()
#we can use the DBConfig class to access the database configuration values
# we will use these values to connect to the database using mysql.connector
def getConnectionWithDB():
    db_host = DBConfig.db_host
    db_user = DBConfig.db_user
    db_port = DBConfig.db_port
    db_password = DBConfig.db_password
    db_name = DBConfig.db_name
    try:
        connection = sql.connect(
            host=db_host,
            user=db_user,
            port=db_port,
            password=db_password,
            database=db_name
        )
        return connection
    except:
        return "connection failed"

# print(getConnectionWithDB())
def insertUserRecord(user_data):
    name = user_data['name']
    email = user_data['email']
    password_hash = user_data['password_hash']
    connection = getConnectionWithDB()
    if connection == "connection failed":
        return False
    else:
        try:
            cursor = connection.cursor()
            # query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            # values = (name, email, password)
            # cursor.execute(query, values)
            cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)", (name, email, password_hash))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except:
            print("Data cannot be inserted")
# define data
data = [{
    'name': 'loki',
    'email': 'lokiloki@gmail.com',
    'password_hash': 'lokesh2004'
},{
    'name': 'sailu',
    'email': 'sailu@gmail.com',
    'password_hash': 'sailu2004'
},{
    'name': 'roxx',
    'email': 'roxx@gmail.com',
    'password_hash': 'roxx2004'
},{
    'name': 'bujji',
    'email': 'bujji@gmail.com',
    'password_hash': 'bujji2004'
}
]
# insert data into database
#for d in data:
    #print(insertUserRecord(d))

def readUserRecords():
    connection=getConnectionWithDB()
    if connection =="connection failed":
        return False
    else:
        cursor=connection.cursor()
        cursor.execute("select * from users")
        data=cursor.fetchall()
        records=[]
        for record in data:
            temp={}
            #print(record)
            temp['id']=record[0]
            temp['name']=record[1]
            temp['email']=record[2]
            temp['password_hash']=record[3]
            temp['is_verified']=record[4]
            temp['created_at']=record[5]
            records.append(temp)
        return records
#print(readUserRecords())

def readUserRecordbyEmail(user_data):
    email=user_data['email']
    connection=getConnectionWithDB()
    if connection=="connection failed":
        return False
    else:
        cursor=connection.cursor()
        cursor.execute("select * from users where email=%s",(email,))
        data=cursor.fetchone()
        #print(data)
        try:
            record={
                "id":data[0],
                "name":data[1],
                "email":data[2],
                "password_hash":data[3],
                "is_verified":data[4],
                "created_at":data[5]
            }
            return record
        except:
            cursor.close()
            connection.close()
            return "No record"
#user_data={"email":"sailu@gmail.com"}
#print(readUserRecordbyEmail(user_data))

def readUserRecordbyId(user_data):
    id = user_data['id']
    connection=getConnectionWithDB()
    if connection=="connection failed":
        return False
    else:
        cursor=connection.cursor()
        cursor.execute("select * from users where id=%s",(id,))
        data=cursor.fetchone()
        try:
            record={
                    "id":data[0],
                    "name":data[1],
                    "email":data[2],
                    "password_hash":data[3],
                    "is_verified":data[4],
                    "created_at":data[5]
                    }
            return record
        except:
               cursor.close()
               connection.close()
               return "No record"
#user_data={"id":1}
#print(readUserRecordbyId(user_data))

def updateNamebyIDorEmail(user_data):
    query_filter=""
    try:
        id=user_data["id"]
        query_filter="id"
    except:
        email=user_data["email"]
        query_filter="email"
    new_name=user_data["new_name"]
    connection=getConnectionWithDB()
    if connection=="connection failed":
        return False
    else:
        cursor=connection.cursor()
        if query_filter=="id":
            query="update users set name=%s where id=%s"
            values=(new_name,id)
        elif query_filter=="email":
            query="update users set name=%s where email=%s"
            values=(new_name,email)
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        return True
#user_data={"id":6,"email":"bujji@gmail.com","new_name":"roxx"}
#print(updateNamebyIDorEmail(user_data))

def updatePasswordbyIDorEmail(user_data):
    query_filter=""
    try:
        id=user_data["id"]
        query_filter="id"
    except:
        email=user_data["email"]
        query_filter="email"
    new_password=user_data["new_password"]
    connection=getConnectionWithDB()
    if connection=="connection failed":
        return False
    else:
        cursor=connection.cursor()
        if query_filter=="id":
            query="update users set password_hash=%s where id=%s"
            values=(new_password,id)
        elif query_filter=="email":
            query="update users set password_hash=%s where email=%s"
            values=(new_password,email)
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        return True
#user_data={"email":"akhil@gmail.com","new_password":"akhil2003"}
#print(updatePasswordbyIDorEmail(user_data))

def updateVerifiedByIdorEmail(user_data):
    query_filter = ""
    try:
        id = user_data['id']
        query_filter = 'id'
    except:
        email = user_data['email']
        query_filter = 'email'
    new_verified = user_data['new_verified']
    connection = getConnectionWithDB()
    if connection == 'Connection Failed':
        return False
    else:
        cursor = connection.cursor()
        if query_filter == "id":
            query = "UPDATE users SET is_verified = %s WHERE id = %s"
            values = (new_verified,id)
        elif query_filter == "email":
            query = "UPDATE users SET is_verified = %s WHERE email = %s"
            values = (new_verified,email)
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        return "done"
#user_data={"email":"roxx@gamil.com","new_password":"akhil_nelli","new_verified":True,"id":7}
#print(updateVerifiedByIdorEmail(user_data))

def generateOTP():
    otp=random.randint(1000,9999)
    return otp
#print(generateOTP())

def sendOTPviaemail():
    pass