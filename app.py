from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np



# Flask utils
from flask import Flask, redirect, url_for, request, render_template,jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)



def model_predict(img_path):
        n= cv2.imread(img_path)
        k=cv2.cvtColor(n, cv2.COLOR_BGR2GRAY)
        #(thresh, im_bw) = cv2.threshold(k, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        thresh = 90
        im_bw = cv2.threshold(k, thresh, 255, cv2.THRESH_BINARY)[1]
        #j=cv2.bitwise_not(k)
        #l=cv2.bitwise_not(j,cv2.COLOR_BGR2GRAY)

          # Run tesseract OCR on image
        text = pytesseract.image_to_string(im_bw, config=config)

        

        patt=re.compile(r'\d{1,2}[ ./-]((J|j)(an|AN)[A-Za-z]*|(F|f)(eb|EB)[A-Za-z]*|(M|m)(AR|ar)[a-z]*|Apr[a-z]*|May[a-z]*|Jun[a-z]*|Jul[a-z]*|Aug[a-z]*|Sep[a-z]*|Oct[a-z]*|Nov[a-z]*|Dec[a-z]*|\d{1,2})[ ./-]?(\d{2,4})+')
        matches=patt.findall(text)
        #print(matches)
        j=0
        am=[]
        #dic={}
        for i in matches:
            print(i)
            j=j+1
            am.append(i)
            #print(j)
            #dic[0]=i
        return am
    
    


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path)

        
        result = jsonify(preds)            
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)

