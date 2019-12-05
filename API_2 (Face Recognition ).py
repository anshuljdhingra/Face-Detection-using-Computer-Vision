
# coding: utf-8

# ## API for matching faces on self recorded video and Passport image

# In[ ]:


# importing required libraries

from flask import Flask, jsonify, request
import cv2
import PIL
import os
import dlib
import face_recognition
import numpy 
import requests
from PIL import Image


# In[ ]:


# Creating function to convert images from recorded video and matches the frame image with passport image

#assigning path
path = os.getcwd()

def face_recog(a,b):
       
    self_vid = cv2.VideoCapture(a)
    success,image = self_vid.read()
    count = 0
    while success:
        cv2.imwrite("static/frame%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = self_vid.read()
#         print('Read a new frame: ', success)
        count += 1    
    
    #Image rotation of cell phone pictures
    img = cv2.imread('static/frame0.jpg')
    num_rows, num_cols = img.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), 90, 1)
    img_rotation = cv2.warpAffine(img, rotation_matrix, (num_cols, num_rows))
    cv2.imwrite("static/frame00.jpg" ,img_rotation)  ## Saving images in folder 'static' in path

      
    #Face Recognition 
    img1 = 'static/frame00.jpg'
    person1 = face_recognition.load_image_file(img1)
    person1_face_encoding = face_recognition.face_encodings(person1)[0]
#     display("Person-1")
#     display(Image(img1))

#      img2 = b
#     person2 = face_recognition.load_image_file(img2)
    person2 = face_recognition.load_image_file(b)
    person2_face_encoding = face_recognition.face_encodings(person2)[0]
#     display("Person-2")
#     display(Image(img2))

    #comparing 2 faces
    results = face_recognition.compare_faces([person1_face_encoding], person2_face_encoding)

    if results[0] == True:
        result = "Matched"
#         print(result)
    else:
        
        result = "Not matched"
#         print(result)      

    
    return result


# In[ ]:


## Function check
# face_recog('static/vid1.mp4','static/img.jpg')
# result


# In[79]:


# Creating API to take video and image as input and gives the face recognition match result

app = Flask(__name__)
@app.route('/VideoUploadAndValidate', methods=['POST'])
def upload_file():
 
    vid = request.files['vid']
    img = request.files['img']
    vid.save(path+"//static//vid.mp4")
    img.save(path+"//static//img.jpg")

    return jsonify({'Face Recognition':face_recog('static/vid.mp4','static/img.jpg')})


app.run(host = '172.19.200.66',port=5000) # change with the IP address

