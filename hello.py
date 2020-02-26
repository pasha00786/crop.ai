from flask import *
import pandas as pd
import numpy as np
import urllib, json
from sklearn.externals import joblib
from mlr_algo import recommendCrop
from disease import classify
import os

app = Flask(__name__)

app.config['COMPRESSOR_DEBUG'] = app.config.get('DEBUG')
app.config['COMPRESSOR_STATIC_PREFIX'] = 'static'
app.config['COMPRESSOR_OUTPUT_DIR'] = 'build'
app.config["IMAGE_UPLOADS"] = './static/img'
app.static_folder = 'static' 
#compress = FlaskStaticCompress(app)

symptoms = {
  
  'BrownSpot' : 'Try Crop Rotation  with recommend Crops and provide balance dose of nitrogen',
  'Healthy'   : 'No remedies required',
  'LeafBlast' : 'Avoid excess dose of fertilizers and eliminate weed hosts',
  'CommonRust': 'Spray Dipthane M-45 spray(0.4%)',
  'LeafSpot'  : 'Destruct plant debris by deep ploughing '
}

@app.route('/')
def index():
    states = {
        'West Bengal': ['Alipurduar', 'Bankura','Bardhaman','Birbhum','Coochbehar','Darjeeling','Dinajpur Dakshin','Dinajpur Uttar','Hooghly','Howrah','Jalpaiguri','Maldah','Medinipur East','Medinipur West','Murshidabad','Nadia','Purulia'],
        'Uttar Pradesh': ['Agra','Aligarh','Allahabad','Ambedkar Nagar','Amethi','Amroha','Auraiya','Azamgarh','Baghpat','Bahraich','Ballia','Balrampur','Banda','Barabanki','Bareilly','Basti','Bijnor','Budaun','Bulandshahr','Chandauli','Chitrakoot','Deoria','Etah','Etawah','Faizabad','Farrukhabad','Fatehpur','Firozabad','Gautam Buddha Nagar','Ghaziabad','Ghazipur','Gonda','Gorakhpur','Hamirpur','Hapur','Hardoi','Hathras','Jalaun','Jaunpur','Jhansi','Kanpur Dehat','Kannauj','Kanpur Nagar','Kasganj','Kaushambi','Kheri','Khushi Nagar','Lalitpur','Lucknow','Maharajganj','Mahoba','Mainpuri','Mathura','Meerut','Mau','Mirzapur','Moradabad','Muzaffarnagar','Pilibhit','Pratapgarh','Rae Bareli','Rampur''Saharanpur','Sambhal','Sant Kabeer Nagar','Sant Ravidas Nagar','Shahjahanpur','Shamli','Shravasti','Siddharth Nagar','Sitapur','Sonbhadra','Sultanpur','Unnao','Varanasi']
    }

    return render_template('home.html', states=states)

@app.route('/login',methods = ['POST', 'GET'])
def login():
  city = ''
  state = request.form.get('state')
  month = int(request.form.get('month'))
  if(state == 'West Bengal'):
    city = 'Kolkata '
  else:
    city = 'Varanasi '
  area = request.form.get('area')
  crops = recommendCrop(city, month)
  return render_template('crop.html', crop_1 = crops[0], crop_2 = crops[1], crop_3 = crops[2], area = area) # just to see what select is

@app.route('/disease')
def disease():
    return render_template('disease.html')

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    model = request.form.get('model')
    if request.method == "POST":

        if request.files:

            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], 'upload.jpg'))
            disease = classify(model)
            # full_filename = os.path.join(app.config['IMAGE_UPLOADS'], 'upload.jpg')

    return render_template("upload_image.html", disease = disease, symptoms = symptoms[disease])

@app.route('/crop/<name>')
def crop(name):
  if(name == 'Wheat'):
    return render_template('crop_depth-wheat.html', crop = name)
  else:
    return render_template('crop_depth-rice.html', crop = name)
if __name__ == '__main__':
   app.run(debug = True, threaded = False)