#Usage: python app.py
import os
 
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.utils import secure_filename
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model
import numpy as np
import argparse
import imutils
import cv2
import time
import uuid
import base64

img_width, img_height = 224, 224
model_path = 'plant_disease_detection'
model = load_model(model_path)
cls ={"Apple___Apple_scab": 0, "Apple___Black_rot": 1, "Apple___Cedar_apple_rust": 2, "Apple___healthy": 3, "Blueberry___healthy": 4, "Cherry_(including_sour)___Powdery_mildew": 5, "Cherry_(including_sour)___healthy": 6, "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": 7, "Corn_(maize)___Common_rust_": 8, "Corn_(maize)___Northern_Leaf_Blight": 9, "Corn_(maize)___healthy": 10, "Grape___Black_rot": 11, "Grape___Esca_(Black_Measles)": 12, "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": 13, "Grape___healthy": 14, "Orange___Haunglongbing_(Citrus_greening)": 15, "Peach___Bacterial_spot": 16, "Peach___healthy": 17, "Pepper,_bell___Bacterial_spot": 18, "Pepper,_bell___healthy": 19, "Potato___Early_blight": 20, "Potato___Late_blight": 21, "Potato___healthy": 22, "Raspberry___healthy": 23, "Soybean___healthy": 24, "Squash___Powdery_mildew": 25, "Strawberry___Leaf_scorch": 26, "Strawberry___healthy": 27, "Tomato___Bacterial_spot": 28, "Tomato___Early_blight": 29, "Tomato___Late_blight": 30, "Tomato___Leaf_Mold": 31, "Tomato___Septoria_leaf_spot": 32, "Tomato___Spider_mites Two-spotted_spider_mite": 33, "Tomato___Target_Spot": 34, "Tomato___Tomato_Yellow_Leaf_Curl_Virus": 35, "Tomato___Tomato_mosaic_virus": 36, "Tomato___healthy": 37}
#model.load_weights(model_weights_path)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['jpg','JPG', 'jpeg','png'])

def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)

def predict(file):
    x = load_img(file, target_size=(img_width,img_height))
    x = img_to_array(x)
    x = np.expand_dims(x, axis=0)
    array = model.predict(x)
    prob_dict = cls
    j=0
    for i in prob_dict:
        prob_dict[i] = array[0][j]
        j += 1
        
    sorted_dict = {}
    sorted_keys = sorted(prob_dict, key=prob_dict.get,reverse=True)  # return the list of key values which are sorted based on their values

    for w in sorted_keys:
        sorted_dict[w] = prob_dict[w]

    res = []

    i = 0
    for d in sorted_dict:
        if(sorted_dict[d] >= 0.026):
          res = d + " ("+str(int(sorted_dict[d]*100))+"%)"
        i+=1
        if(i==1):
          break
        
    return res

def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def template_test():
    return render_template('template.html', label='')

@app.route("/predict/", methods=['GET', 'POST'])
def upload_file():
    label = ''
    if request.method == 'POST':
        import time
        start_time = time.time()
        file = request.files['file']
        print(file.filename)
        print(file)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                result = predict(file_path)
                print(result)
                print(file_path)
                filename = my_random_string(6) + filename

                os.rename(file_path, os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print("--- %s seconds ---" % str (time.time() - start_time))
                return render_template('predict.html', label=result, imagesource='../uploads/' + filename)
            except ValueError:
                return "Please valid image"
        else:
            print("Not a file")
    else:
        print("request.method error")
    return None

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/uploads':  app.config['UPLOAD_FOLDER']})

if __name__ == '__main__':
    app.run(debug=True)