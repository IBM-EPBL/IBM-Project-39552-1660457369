import cv2
import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from Alert import send_alert, is_valid_number
import sys
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv
load_dotenv('.env')

# Loading the model
model = load_model(os.getenv('MODEL_PATH'))

# Predict the image with Path as Parameters
def predict(img_path):
  img = image.load_img(img_path,target_size=(64,64))
  x = image.img_to_array(img)
  x = np.expand_dims(x,axis=0)
  pred = model.predict(x).flatten()[0]
  
  return pred


# Main detect Function
def detect(path=0,to:bool=False):
  
  '''
  This is function is for Detecting The Forest Fire In the live Webcam
  Model is Loaded and path can be changed with making changes in .env file
  this function will awake the alarm if it finds the Fire
  
  accepts a path parameter which you can use to load local file for sample prediction
  Default = Liveweb cam
  accepts a to parameter which you can use to load To Number for Alert
  Default = which is prebuild Number
  
  will write the final image predicted in Name Of : Files/Image.jpg
  and write the prediction in a file named of : Files/prediction.txt
  
  Press 'q' to stop the Program
  '''
  
  video = cv2.VideoCapture(path)
  
  
  if not video.isOpened():
    print("Could not open webcam")
    exit()
  
  while True:
      success,frame = video.read()    
      cv2.imwrite('Files/Image.jpg',frame)
      pred = predict('Files/Image.jpg')
      
      with open('Files/prediction.txt','w') as f:
        f.write(f"{str(pred)}\n1")
      
      if not pred:
        cv2.imshow('Video',frame)
        print('No Issues')
      else:
        cv2.putText(frame,"Fire Detected!!!",(50,70),fontFace= cv2.FONT_HERSHEY_SIMPLEX,thickness=3,fontScale=2,color=(0,0,255))
        cv2.imshow('Video',frame)
        print('There is Fire!!')
        
        if to:
          send_alert(To=to)
        else:
          send_alert()
      
      
      if cv2.waitKey(1)&0xFF == ord('q'):
          break
  
  video.release()
  cv2.destroyAllWindows()
  
  with open('Files/prediction.txt','w') as f:
        f.write(f"0\n0")
  
  print("Program Closing...")


if __name__=="__main__":
  
  path = 0
  to = False
  
  # For To Number
  if '--to' in sys.argv:
      to = sys.argv[(sys.argv.index('--to')) + 1]
      if not is_valid_number(to):
        print('Enter a valid Twilio Verified Number')
        exit(0)
      
  
  # For test video path
  if '--path' in sys.argv:
      path = sys.argv[(sys.argv.index('--path')) + 1]
  
  # For pre-build Test vidwo    
  if 'test' in sys.argv:
      path = 'Files/Test_Video_2.mp4'
  
  # Primary Livecam Start
  detect(path,to)
  
