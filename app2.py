
@app.route('/login',methods=['POST'])
def index():
    if request.method == 'POST':
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
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList
        encodeListKnown = findEncodings(images)
        print('Encodig Complete')
       
        cap = cv2.VideoCapture(0)
       
        while True:
            
            
            success, img = cap.read()
            imgs = cv2.resize(img,(0,0),None,0.25,0.25)
            imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
            facesCurFrame = face_recognition.face_locations(imgs)
            encodesCurFrame = face_recognition.face_encodings(imgs,facesCurFrame)

            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            
                
                
                matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
                faceDis = round(faceDis[0],2)
                print(faceDis)
              
                if faceDis <= 0.43:
                   
                 
                   print("Fcae Recognized Sochima")
                   name = 'Sochima'
                   y1,x2,y2,x1 = faceLoc
                   y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                   cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                   cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                   cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                
                   cur = mysql.connection.cursor()
                   cur.execute("INSERT INTO attendance(matno, name,course) VALUES(%s, %s)", (matno, name,course))
                   mysql.connection.commit()
                   cur.close()
                   marked = 'Attendance have been marked Sucessfullyy'
                   
                   return marked
                
                elif faceDis>= 0.70:
                    
                 
                    print("face Recognized Unix")
                    name = 'Unix'
                    y1,x2,y2,x1 = faceLoc
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
   
                else:
                    
                  
                  
                    print("Face Not Found")
                    name = 'Not Found in databse'
                    y1,x2,y2,x1 = faceLoc
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            cv2.imshow('webcam', img)
            key = cv2.waitKey(1)
            if key == 27:
               break
      
       
    
        cap.release()
        cv2.destroyAllWindows()

	

if __name__ == '__main__':
	app.run(debug=True)