
from flask import Flask,render_template,url_for,request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
import numpy as np
#import face_recognition 
#import os



app = Flask(__name__) 



@app.route('/')
def index():
    return render_template("index.html")





           

        
if __name__ == '__main__':
	app.run(debug=True)
