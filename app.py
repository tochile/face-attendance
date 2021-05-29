
from flask import Flask,render_template,url_for,request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
import numpy as np
#import face_recognition 
import os
import cv2


app = Flask(__name__) 
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login',methods=['POST'])
def login():
    
    username = request.form['username']
    password = request.form['password']
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * from Users where binary username=%s and binary password=%s",[username,password])
    if(result>0):
        return render_template("login.html", username=username)
    else:
        error = 'failed'
        return render_template("index.html", error=error)

@app.route('/mark_attendance',methods=['GET', 'POST'])
def mark_attendance():
    
    if request.method == 'POST':

        
        matno = request.form['matno']
        course = request.form['course']
        path = '../people'
        images = []
        classNames = []
        mylist = os.listdir(path)
        for c1 in mylist:
            
            curImg = cv2.imread(f'{path}/{c1}')
            images.append(curImg)
            classNames.append(os.path.splitext(c1)[0])

        def findEncodings(images):
            
           
            encodeList = []
            for img in images:
                img =  cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
               # encode = face_recognition.face_encodings(img)[0]
               # encodeList.append(encode)
            return encodeList
        encodeListKnown = findEncodings(images)
        print('Encodig Complete')
       
        cap = cv2.VideoCapture(0)
       
        while True:
            
            success, img = cap.read()
            imgs = cv2.resize(img,(0,0),None,0.25,0.25)
            imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
           # facesCurFrame = face_recognition.face_locations(imgs)
            #encodesCurFrame = face_recognition.face_encodings(imgs,facesCurFrame)

            #for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            
                
                
               # matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                #faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
              #  faceDis = round(faceDis[0],2)
              #  print(faceDis)
              
               # if faceDis >= 0.70:
                   
                 
                  # print("Fcae Recognized Sochima")
                  # name = 'Unix'
                  # status = 'Present'
                 
               #    y1,x2,y2,x1 = faceLoc
               #    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                   cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                   cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                   cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                
                   cur = mysql.connection.cursor()
                   cur.execute("INSERT INTO attenders(matno, name,course,Status) VALUES(%s, %s, %s, %s)", (matno, name,status,course))
                   mysql.connection.commit()
                   cur.close()
                   marked = 'Attendance have been marked Sucessfullyy'
                   
                   return marked
                   return render_template("login.html", marked=marked)
                
                elif faceDis<= 0.70:
                    
                 
                    print("face Recognized Unix")
                    name = 'Sochima'
                    status = 'present'
                    y1,x2,y2,x1 = faceLoc
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    marked = 'Attendance have been marked Sucessfullyy'
                   
                    return marked
                    #return render_template("login.html", marked=marked)
                else:
                    
                  
                  
                    print("Face Not Found")
                    name = 'Not Found in databse'
                    y1,x2,y2,x1 = faceLoc
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                     
                    marked = 'No Record Found on Database'
                    return marked
                    #return render_template("login.html", marked=marked)
            cv2.imshow('webcam', img)
            key = cv2.waitKey(1)
            if key%256 == 27:
               print("Press ESC key")
               break
      
       
    
    cap.release()
    cv2.destroyAllWindows()
        
@app.route('/admin')
def admin():
    return render_template("admin.html")
       
@app.route('/admin_login',methods=['POST'])
def admin_login():
    
        
        user = request.form['username']
        pass1 = request.form['pass']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * from lecturer where binary username=%s and binary password=%s",[user,pass1])
        if(result>0):
            
            return render_template("adm_login.html", user=user)
        else:
        
            error = 'failed'
            return render_template("admin.html", error=error)

    
@app.route('/view_attendance',methods=['POST'])
def view_attendance():
    
    cur = mysql.connection.cursor()
    result1 = cur.execute("SELECT * from attenders")
    if(result1>0):
        
        attendance = cur.fetchall()
            
        return render_template("view_attendance.html", attendance=attendance)
    
        
           

        
if __name__ == '__main__':
	app.run(debug=True)