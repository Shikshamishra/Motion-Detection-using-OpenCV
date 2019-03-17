import cv2
import numpy as np
import os
from twilio.rest import Client
from credentials import account_sid, auth_token, my_cell, my_twilio
from playsound import playsound
def main():
    w=640
    h=480
    
    c=cv2.VideoCapture(0)
    c.set(3,w)
    c.set(4,h)
    
    if c.isOpened():
        r,fr=c.read()
    else:
        r=False
    r,fr1=c.read()
    r,fr2=c.read()
    while r:
        #print("Hiee")
        b=cv2.absdiff(fr1,fr2)
        fr2c=cv2.cvtColor(b,cv2.COLOR_BGR2GRAY)
        blur=cv2.GaussianBlur(fr2c,(5,5),0)
        r,thresold=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
        dil=cv2.dilate(thresold,np.ones((3,3),np.uint8),iterations=10)
        er=cv2.erode(dil,np.ones((3,3),np.uint8),iterations=10)
        img,con,h=cv2.findContours(er,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print(type(h))
        # print(con)
        # print("Type of connn = " + str(type(con)))
        # print(len(con))
        if(len(con) >= 10):
            print("motion")
            playsound('C:\\Users\\SHIKSHA MISHRA\\Desktop\\openCv\\B.mp3')
            client = Client(account_sid, auth_token)
            my_msg = "someone is in your private area"
            message = client.messages.create(to=my_cell, from_=my_twilio,
                                     body=my_msg)
        else:
            print("no Motion")
        cv2.drawContours(fr1,con,-1,(255,0,0),2)
        cv2.imshow("Normal", fr2)
        cv2.imshow("Output", fr1)
        if cv2.waitKey(1)==27:
            
            break
        fr1=fr2
        r,fr2=c.read()
    cv2.destroyAllWindows()
    c.release()
if __name__=="__main__":
    main()

