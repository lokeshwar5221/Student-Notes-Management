from config import Config
import mysql.connector as sql
import random 
import smtplib
from email.message import EmailMessage
from flask import Flask,render_template,redirect,url_for,request,session
import bcrypt
app = Flask(__name__)
app.secret_key="lokesh@2004"

DBConfig = Config()
from_email = DBConfig.from_email
email_app_password = DBConfig.email_app_password
OTP=0
#Encode --> Str to Bytes
#Decode --> Bytes to Str
#gensalt -->is it used to generate a key
#how many rounds this key to iterate
#gensalt(4)
def generateHash(text):
    btext=text.encode('utf-8')
    cipher_text=bcrypt.hashpw(btext,bcrypt.gensalt(4))
    return cipher_text
    #return cipher_text.decode('utf-8')
    #print(cipher_text,len(cipher_text))
    #print(text[0],btext[0])#returns encoded value
    #print(typr(btext)) 
    #bcrypt.hashpw 
#text='lokesh'
#print(generateHash(text))

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

def sendOTPviaemail(to_email,otp):
    message = EmailMessage()
    message['Subject'] = "OTP Notification"
    message['From'] = from_email
    message['To'] = to_email
    message.set_content(
        f"Your OTP is {otp}"
    )
    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login(from_email,email_app_password)
        server.send_message(message)
    return True

#sendOTPviaemail('sakethreddy.kallepu@gmail.com',5423)
def validateData(user_data):
    errors =[]
    name=user_data['name']
    email=user_data['email']
    password = user_data['password']
    confirm_password = user_data['confirm_password']
    if name is None or len(name)<2:
        errors.append("Invalid Email")
    if email is None or len(email)<5:
        errors.append("Invalid Email")
    if password is None or len(password)<5:
        errors.append("Invalid Password")
    if password!=confirm_password:
        errors.append("Password mismatch")
        errors.append("Invalid Email")
    return errors
def verifyDeplicatebyEmail(user_data):
    #email=user_data['email']
    record=readUserRecordbyEmail(user_data)
    if (record=="No record"):
        return False #duplicates are not found
    else:
        return True #duplicate records are found
user_data = {'id':2,
             'name':"sailu",
             'email':'sailu@gmail.com',
             'password':'sailu2004',
             'confirm_password':'sailu2004',
             'verified':True}
#print(updateNamebyIDorEmail(user_data))
#print(updateVerifiedByIdorEmail(user_data))
#print(generateOTP())
#print(validateData(user_data))
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/register',methods=['GET','POST'])
def register():
    global OTP
    if (request.method =="GET"):
        return render_template('register.html')
    elif (request.method=="POST"):
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password  = request.form['confirm_password']
        user_data = {
            "name":name,
            "email":email,
            "password":password,
            "confirm_password":confirm_password
        }
        errors = validateData(user_data)
        if len(errors)>0:
            return render_template('register.html',errors=errors)
        else:
            is_duplicate = verifyDeplicatebyEmail(user_data)
            if is_duplicate == False:
                #if there is no account the password will be converted into hash passwprd
                session['otp']=generateOTP()
                #OTP=generateOTP()
                password_hash=generateHash(user_data['password'])
                name=user_data['name']
                email=user_data['email']
                status=insertUserRecord({
                    'name':name,
                    'email':email,
                    'password_hash':password_hash
                })
                if status==True:
                    session['username']=email
                    session['otp']=OTP
                    sendOTPviaemail(email,OTP)
                    return redirect('/verify')
                    #return render_template('register.html',res="Registration successfull completed")
                else:
                    return render_template('register.html',err="Registration Failed")
            else:
                return render_template('register.html',err="Account already Exists")
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/verify',methods=['GET','POST'])
def verify():
    global OTP
    if request.method=="GET":
        return render_template('verify.html')
    elif request.method=="POST":
        otp=request.form['otp']
        otp=int(otp)
        if otp==OTP:
            is_verify=True
            updateVerifiedByIdorEmail({'email':session['username'],'is_verified':is_verify})
            return redirect('/login')
        else:
            return render_template('verify.html',err="Invalid OTP")

if (__name__ == "__main__"):
    app.run(host="0.0.0.0",
            port = 5003,
            debug=True)

#Registration flow:

#User -->registration.html --> registration form-->POST -->Collecting data-->Validating-->Veriifing -->Password to Password Hash -->MySQL Table

#HTML<-->Python<-->MySQL
'''
@app.route('/register',methods=['GET','POST'])
def register():
    if (request.method =="GET"):
        return render_template('register.html')
    elif (request.method=="POST"):
        collecting userdata()
        validate userdata()
        display errors()
        status=verifyaccountexist()
        if status:
            insertrecord()
        else:
            display error message()
''' 