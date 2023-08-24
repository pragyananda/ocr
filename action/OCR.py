import os, io
import cv2
import numpy as np
from google.cloud import vision
# from googletrans import Translator
import pandas as pd
from .image_preprocessing import *
from .extract_entities import *
json_file_path = os.path.join(os.path.dirname(__file__), 'ocr_project_394905_f4d1a5998351.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_file_path
client = vision.ImageAnnotatorClient()

def detect_text(img):
    img=cv2.imencode(".jpg",img)[1].tobytes()
    img=vision.Image(content=img)
    image_context = vision.ImageContext(language_hints=["en", "hi"])
    response=client.document_text_detection(image=img,image_context=image_context)
    return response.text_annotations[0].description.replace("\n"," ").replace(".", "")

def prepare_image(image,coords):
    h,w,_=image.shape
    mask=np.zeros((10,w,3),np.uint8)
    img=mask
    text=[]
    for c in coords:
        temp_img=image[int(c[0]*h):int(c[1]*h),1:w]
        text.append(detect_text(temp_img))
        img=np.uint8(np.concatenate((img,cv2.resize(temp_img, (w,temp_img.shape[0])),mask),axis=0))
    return img,text


def do_ocr(frame):
    coords1=[[0.2, 0.25],[0.25, 0.28 ],[0.272 , 0.302],[0.295, 0.325]]
    coords3=[[0.235, 0.268],[0.263, 0.29 ],[0.288 , 0.32],[0.32, 0.345]]
    image,angle=auto_rotate_image(frame)
    image=crop_image_automatically(image)
    if angle <-0.5 or angle> 0.5:
        image,text=prepare_image(image,coords1)
    elif 0.5 > angle >-0.5 :
        image,text=prepare_image(image,coords3)
    # print(text)
    details=extract_info(" ".join(text))
    return details

# def perform_ocr(file_path):
#     text={}
#     for img in [i for i in os.listdir(file_path) if not i.endswith("1.jpg")][:1]:
#         text[img]=do_ocr(f"BCA2015/{img}")
#     data=pd.DataFrame(text)
#     return data

# print(do_ocr(cv2.imread("media\Aashi Agrawal.jpg")))
