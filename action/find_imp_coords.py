import os
import cv2
import numpy as np
import pandas as pd
main_coord = []
i=os.listdir("./")
i=[j for j in i if j.endswith(".jpg")]
frame=cv2.imread(f"./{i[np.random.randint(i.__len__())]}")
def crop_image_automatically(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    most_frequent_number=np.average(np.bincount(image.ravel()).argsort()[-10:]).astype(int)
    element=cv2.getStructuringElement(cv2.MORPH_RECT,(10,1))
    _,thresh=cv2.threshold(image,most_frequent_number,most_frequent_number,cv2.THRESH_BINARY_INV)
    mask=np.full(np.subtract(thresh.shape,40).astype(tuple),255,np.uint8)
    mask = np.pad(mask, pad_width=20, mode='constant', constant_values=0)
    image=cv2.bitwise_and(mask, thresh)
    image=cv2.dilate(image,element)
    x,y,w,h=cv2.boundingRect(max(cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0],key=cv2.contourArea))
    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),5)
    
    return frame[y:y+h,x:x+w]
image=crop_image_automatically(frame)
image=cv2.resize(image,(720,800))
image1=image.copy()
init_cord={"x":0, "y":0}
last_cord={"x":0,"y":0}
coords=[]
state=False
def click_event(event,x,y,flags,param):
    global image,image1,state
    
    if event==cv2.EVENT_LBUTTONDOWN:
        state=True
        init_cord["x"]=x
        init_cord["y"]=y
        
    if event==cv2.EVENT_MOUSEMOVE:
        image1=image.copy()
        if state:
            image1=cv2.rectangle(image1,(init_cord["x"],init_cord["y"]),(x,y),(255,0,0),1)
        
    if event == cv2.EVENT_LBUTTONUP:
        state=False
        last_cord["x"]=x
        last_cord["y"]=y
        coords.append([init_cord["x"],init_cord["y"],x,y])
        image=cv2.rectangle(image,(init_cord["x"],init_cord["y"]),(x,y),(255,0,0),1)
        
while True:
    cv2.imshow("image", image1)
    a,b,c=image1.shape
    
    cv2.setMouseCallback("image",click_event)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print(coords)
        break
cv2.destroyAllWindows()
main_coord.append(np.divide(coords,[image.shape[1],image.shape[0],image.shape[0],image.shape[0]]))

data=pd.DataFrame()
for i,_ in enumerate(main_coord):
    data=pd.concat([data,pd.DataFrame(np.array(main_coord[i]))],axis=1)
coords=pd.DataFrame(np.round([data[0].T.mean(),data[1].T.mean(),data[2].T.mean(),data[3].T.mean()],decimals=2)).T.values
print(coords)