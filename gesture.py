import cv2
import numpy as np

def gest(cam):
    kernelOpen = np.ones((5,5))
    kernelClose = np.ones((20,20))

    lowerBound = np.array([30,140,150])
    upperBound = np.array([130,250,250])

    ret, img = cam.read()
    img = cv2.resize(img,(400,300))
    img = cv2.flip(img, 1)

    mask=cv2.inRange(img,lowerBound,upperBound)

    maskOpen = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose= cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal = maskClose
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    cx = 0
    cy = 0
    pinchFlag = 0

    if len(conts) == 2:
        if pinchFlag == 1:
            pinchFlag=0
        x1,y1,w1,h1 = cv2.boundingRect(conts[0])
        x2,y2,w2,h2 = cv2.boundingRect(conts[1])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
        cx1 = x1+w1/2
        cy1 = y1+h1/2
        cx2 = x2+w2/2
        cy2 = y2+h2/2
        cx = (cx1+cx2)/2
        cy = (cy1+cy2)/2
        cv2.line(img, (int(cx1),int(cy1)),(int(cx2),int(cy2)),(255,0,0),2)
        cv2.circle(img, (int(cx),int(cy)),2,(0,0,255),2)
    elif len(conts) == 1:
        x,y,w,h = cv2.boundingRect(conts[0])
        if pinchFlag==0:
            pinchFlag=1
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cx = x+w/2
        cy = y+h/2
        cv2.circle(img,(int(cx),int(cy)),int((w+h)/4),(0,0,255),2)
        
    cv2.imshow("cam",img)
    cv2.waitKey(30)
    return [cx,cy,pinchFlag]