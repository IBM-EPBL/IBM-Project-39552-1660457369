import cv2
import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from Alert import send_alert
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv
load_dotenv('.env')


model = load_model(os.getenv('MODEL_PATH'))

def predict(img_path):
  img = image.load_img(img_path,target_size=(64,64))
  x = image.img_to_array(img)
  x = np.expand_dims(x,axis=0)
  pred = np.argmax(model.predict(x))
  
  return pred

def detect(path=0):
  video = cv2.VideoCapture(path)
  
  while True:
      success,frame = video.read()    
      cv2.imwrite('Image.jpg',frame)
      pred = predict('Image.jpg')
      
      if pred:
        cv2.imshow('Video',frame)
        print('No Issues')
      else:
        cv2.putText(frame,"Fire Detected!!!",(50,80),fontFace= cv2.FONT_HERSHEY_SIMPLEX,thickness=2,fontScale=2,color=(0,0,255))
        cv2.imshow('Video',frame)
        print('There is Fire!!')
        send_alert()
      
      if cv2.waitKey(1)&0xFF == ord('q'):
          break
  
  video.release()
  cv2.destroyAllWindows()
  


if __name__=="__main__":
  detect('Files/Test_Video_2.mp4')
