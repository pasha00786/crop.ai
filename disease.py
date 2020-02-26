import numpy as np
import pickle
import cv2
import os
from os import listdir
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

EPOCHS = 10
INIT_LR = 1e-3
BS = 32
default_image_size = tuple((256, 256))
image_size = 0
directory_root = './static/img/'
width=256
height=256
depth=3

def convert_image_to_array(image_dir):
    try:
        image = cv2.imread(image_dir)
        if image is not None :
            image = cv2.resize(image, default_image_size)
#             image = np.expand_dims(image, 3)
#             print(image.shape)
            return img_to_array(image)
        else :
            return np.array([])
    except Exception as e:
        print(f"Error : {e}")
        return None

def classify(crop):
  label = {}
  image_list = []
  img = directory_root + 'upload.jpg'
  image_list.append(convert_image_to_array(img))
  np_image_list = np.array(image_list, dtype=np.float16) / 225.0
  if(crop == 'Rice'):
    model = pickle.load(open('./rice_model.pkl', 'rb'))
    label = {0: 'BrownSpot', 1: 'Healthy', 2: 'LeafBlast', 3: 'LeafBlast'}
  else:
    model = pickle.load(open('./maize_model.pkl', 'rb'))
    label = {0: 'LeafSpot', 1 : 'CommonRust', 2: 'Healthy'}
  
  opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
  model.compile(loss="binary_crossentropy", optimizer=opt,metrics=["accuracy"])
  result = model.predict(np_image_list)
  return label[np.argmax(result[0])]