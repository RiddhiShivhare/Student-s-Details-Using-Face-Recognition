from flask import Flask, render_template
from flask_cors import CORS
import cv2
import numpy as np
import face_recognition
import os
import datetime
import mysql.connector
import glob

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

path='imageAttendance' #folder where all the images of registered students are saved
images=[]
classnames=[]
classUniqId=[]  #List that stores Unique Id of student
classname=[] #List that stores Names of Student
myList= os.listdir(path)

for cls in myList:
    curImg=cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classnames.append(os.path.splitext(cls)[0])

for name in classnames:
    data= name.split(" ",1)
    classUniqId.append(data[0])  #separating id and name from photo name
    classname.append(data[1])


def markAttendance(name): #Function to mark attendance in database
            conn=mysql.connector.connect(host="localhost" , user='root' , passwd='alapk26021973@', database="mysql") #connecting to MySql
            cursor=conn.cursor()
            nowd=datetime.datetime.now()  #recording the current time
            dtStringY=nowd.strftime("%D %H:%M:%S")
            dtString = dtStringY.split(" ") #spliting the string
            sql=("INSERT INTO attendance (Name, Date, Time) " #Inserting date time and name in sql database
            "VALUES (%s,%s,%s)")
            d=(name,dtString[0],dtString[1])
            cursor.execute(sql,d)
            conn.commit()


def getDetails(name): #Function to fetch the details from database
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="alapk26021973@", database="studentdb") #connecting to database
    mycursor = mydb.cursor()
    mycursor.execute("Select * from studentdetails")
    myresult = mycursor.fetchall() #fetching all rows of the table
    for row in myresult:
        if name in row[1]: #if name is in row then return that row
            return(row)



encodeListKnown=[] #List of List to store the encoding values
with open("encoding.txt", "r") as f: #Reading the encoding text file
     while True:
      lines = f.readline()
      if(lines==''):
         break
      encode=[]
      encode.append(float(lines))
      for i in range(127):
         lines = f.readline()
         encode.append(float(lines))
      encodeListKnown.append(encode)


@app.route("/")
def hello_world():
    while True:
        row=0
        img_dir = 'uploads' #Floder where the Live Scanned Picture will get uploaded
        data_path = os.path.join(img_dir, '*g')
        files = glob.glob(data_path)
        for i in files:
            img = cv2.imread(i) #reading the image
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurr = face_recognition.face_locations(img)
        encodeCurr = face_recognition.face_encodings(img, faceCurr)

        for enf, floc in zip(encodeCurr, faceCurr):
            matches = face_recognition.compare_faces(encodeListKnown, enf)
            faceDis = face_recognition.face_distance(encodeListKnown, enf)

            matchIndex = np.argmin(faceDis)
            min = np.amin(faceDis)

            if matches[matchIndex]:
                name = classname[matchIndex].upper()

                if (min < 0.5100000000000000):  # Threshold value
                    row = getDetails(name) #calling the getDetails and markAttendance functions
                    markAttendance(name)

        if(row):
            return render_template("MainPage.html", data=row)  #if person is registered then displaying the main page
        else:
            return render_template("NoRecord.html")  #else asking the admin to get the student registered


app.run("localhost", port=5000, debug=True)